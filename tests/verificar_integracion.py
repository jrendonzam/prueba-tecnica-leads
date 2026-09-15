"""Verificación real aislada: API HTTP y MySQL 8 instalado en Windows.
Ejecutar: python tests/verificar_integracion.py
No utiliza credenciales ni servicios de base de datos existentes.
"""
from pathlib import Path
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.procesar_leads import cargar_datos, limpiar_datos, enviar_muestra_api


def puerto_libre():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def verificar_api():
    puerto = puerto_libre()
    # Desactivar únicamente el fallo aleatorio para hacer la prueba reproducible.
    codigo = f"import src.api as api; import uvicorn; api.random.random=lambda: 1; uvicorn.run(api.app, host='127.0.0.1', port={puerto}, log_level='error')"
    proceso = subprocess.Popen([sys.executable, "-c", codigo], cwd=ROOT)
    previo = os.environ.get("CRM_API_URL")
    try:
        url = f"http://127.0.0.1:{puerto}"
        for _ in range(100):
            try:
                if requests.get(url + "/api/desarrollos", timeout=1).ok:
                    break
            except requests.RequestException:
                time.sleep(0.1)
        else:
            raise RuntimeError("La API no inició")
        os.environ["CRM_API_URL"] = url + "/api/leads"
        resultado = enviar_muestra_api(limpiar_datos(cargar_datos()), 16)
        assert resultado["enviados"] == 15 and resultado["fallidos"] == [13], resultado
        payload = limpiar_datos(cargar_datos()).head(1).to_dict(orient="records")[0]
        assert requests.post(url + "/api/leads", json=payload, timeout=3).status_code == 401
        print("API HTTP: 15/16 enviados; lead 13 rechazado por 400; reintento 429 y 401 verificados.")
    finally:
        if previo is None:
            os.environ.pop("CRM_API_URL", None)
        else:
            os.environ["CRM_API_URL"] = previo
        proceso.terminate()
        proceso.wait(timeout=15)


def verificar_mysql():
    mysql = shutil.which("mysql")
    if not mysql:
        raise RuntimeError("Se necesita mysql y mysqld de MySQL 8 en PATH")
    mysqld = str(Path(mysql).with_name("mysqld.exe" if os.name == "nt" else "mysqld"))
    base = ROOT / ".mysql-test"
    base.mkdir(exist_ok=True)
    # Conservar directorio temporal y log para inspección; no borrar archivos.
    datos = Path(tempfile.mkdtemp(prefix="run-", dir=base))
    puerto = puerto_libre()
    subprocess.run([mysqld, "--no-defaults", "--initialize-insecure", f"--datadir={datos}"], check=True, timeout=120, capture_output=True)
    servidor = subprocess.Popen([mysqld, "--no-defaults", f"--datadir={datos}", "--bind-address=127.0.0.1", f"--port={puerto}", "--mysqlx=OFF"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    argumentos = [mysql, "--no-defaults", "--protocol=TCP", "-h127.0.0.1", f"-P{puerto}", "-uroot", "--default-character-set=utf8mb4", "--batch", "--skip-column-names"]
    def consulta(sql):
        return subprocess.run(argumentos, input=sql, encoding="utf-8", capture_output=True, check=True, timeout=30).stdout.strip()
    try:
        for _ in range(100):
            try:
                consulta("SELECT 1;")
                break
            except subprocess.CalledProcessError:
                time.sleep(0.2)
        else:
            raise RuntimeError("MySQL no inició; consultar log en " + str(datos))
        schema = (ROOT / "sql/schema.sql").read_text(encoding="utf-8")
        seed = (ROOT / "sql/seed.sql").read_text(encoding="utf-8")
        queries = (ROOT / "sql/queries.sql").read_text(encoding="utf-8")
        consulta("CREATE DATABASE prueba; USE prueba;" + schema + seed)
        assert consulta("USE prueba; SELECT COUNT(*) FROM leads;") == "640"
        assert consulta("USE prueba; SELECT COUNT(*) FROM desarrollos;") == "6"
        salida = consulta("USE prueba;" + queries)
        assert salida
        # Comprobar restricciones reales.
        for sql in ("UPDATE leads SET desarrollo_id=99 WHERE id=1;", "UPDATE leads SET presupuesto=-1 WHERE id=1;", "UPDATE leads SET email=(SELECT email FROM (SELECT email FROM leads WHERE id=2) AS x) WHERE id=1;"):
            try:
                consulta("USE prueba;" + sql)
            except subprocess.CalledProcessError:
                pass
            else:
                raise AssertionError("Restricción no aplicada: " + sql)
        # Datos controlados para comprobar semántica de las cuatro consultas.
        consulta("CREATE DATABASE bordes; USE bordes;" + schema + "INSERT INTO desarrollos VALUES (1,'A','Ciudad','Estado'),(2,'B','Ciudad','Estado');")
        filas = [(1,"NOW()","NUEVO",100),(2,"NOW() - INTERVAL 30 DAY","CONTACTADO",300),(3,"NOW() - INTERVAL 31 DAY","NUEVO",500),(4,"NOW() + INTERVAL 1 DAY","NUEVO",700),(5,"NOW()","PERDIDO",900)]
        consulta("SET timestamp=1789488000; USE bordes;" + "".join(f"INSERT INTO leads (id,nombre,email,origen,fecha_registro,estatus,presupuesto,desarrollo_id) VALUES ({i},'Lead','{i}@test','Web',{fecha},'{estado}',{presupuesto},1);" for i,fecha,estado,presupuesto in filas))
        import re
        sentencias = [s.strip() for s in re.sub(r"--[^\n]*", "", queries).split(";") if s.strip()]
        respuestas = [consulta("SET timestamp=1789488000; USE bordes;" + s).splitlines() for s in sentencias]
        assert {r.split("\t")[0] for r in respuestas[0]} == {"1", "2"}
        assert respuestas[1] == ["Web\t5"]
        assert len(respuestas[2]) == 5
        assert respuestas[3] == ["1\tA\t5\t500.00", "2\tB\t0\tNULL"], respuestas[3]
        print("MySQL: 640 leads, 6 desarrollos, Q1-Q4 y restricciones validados.")
    finally:
        try:
            consulta("SHUTDOWN;")
            servidor.wait(timeout=20)
        except Exception:
            servidor.terminate()
            servidor.wait(timeout=20)


if __name__ == "__main__":
    verificar_api()
    verificar_mysql()
