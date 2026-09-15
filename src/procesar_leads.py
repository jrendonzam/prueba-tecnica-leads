"""
Módulo de Procesamiento y Limpieza de Leads
Completa las funciones indicadas para limpiar, validar y generar métricas del dataset.
"""
import argparse
import json
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os
import pandas as pd
import requests

DATA_IN = os.path.join(os.path.dirname(__file__), "..", "data", "leads.csv")
DATA_OUT = os.path.join(os.path.dirname(__file__), "..", "data", "leads_limpios.csv")

def cargar_datos() -> pd.DataFrame:
    """1. Cargar el dataset crudo."""
    # Leer telefonos como texto conserva ceros iniciales y evita decimales.
    df = pd.read_csv(DATA_IN, dtype={"telefono": "string"})
    print(f"Total registros cargados: {len(df)}")
    return df

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    2. Limpieza de datos:
       - Eliminar registros duplicados considerando el campo email.
       - Descartar registros con email vacío.
       - Normalizar los valores de estatus a: NUEVO, CONTACTADO, EN_SEGUIMIENTO, CONVERTIDO, PERDIDO.
       - Rellenar valores nulos en la columna presupuesto con 0 o el valor promedio.
    """
    requeridas = {"id", "nombre", "email", "telefono", "origen", "fecha_registro", "estatus", "presupuesto", "desarrollo_id"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Columnas faltantes: {sorted(faltantes)}")
    df_limpio = df.copy()
    # Normalizar correos y conservar la primera fila de cada correo.
    df_limpio["email"] = df_limpio["email"].astype("string").str.strip().str.lower()
    df_limpio = df_limpio.loc[
        df_limpio["email"].notna() & df_limpio["email"].ne("")
    ].drop_duplicates(subset="email", keep="first").copy()

    # Convertir las variantes del CSV a los cinco estatus permitidos.
    estatus = (
        df_limpio["estatus"].astype("string").str.strip().str.upper()
        .str.replace(r"[\s-]+", "_", regex=True)
        .replace({
            "SEGUIMIENTO": "EN_SEGUIMIENTO",
            "CERRADO_GANADO": "CONVERTIDO",
            "NO_INTERESADO": "PERDIDO",
            "DESCARTADO": "PERDIDO",
        })
    )
    permitidos = {"NUEVO", "CONTACTADO", "EN_SEGUIMIENTO", "CONVERTIDO", "PERDIDO"}
    desconocidos = ~estatus.isin(permitidos)
    if desconocidos.any():
        raise ValueError(f"Estatus sin equivalencia definida: {estatus[desconocidos].tolist()}")
    df_limpio["estatus"] = estatus

    # Sustituir presupuestos nulos o no numericos por cero.
    df_limpio["presupuesto"] = pd.to_numeric(
        df_limpio["presupuesto"], errors="coerce"
    ).fillna(0)
    # Distinguir ISO (año primero) de fechas locales (día primero).
    def normalizar_fecha(valor):
        texto = str(valor).strip()
        for formato in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(texto, formato).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        raise ValueError(f"Fecha inválida: {texto}")

    df_limpio["fecha_registro"] = df_limpio["fecha_registro"].map(normalizar_fecha)
    df_limpio["telefono"] = df_limpio["telefono"].astype("string").fillna("").str.strip()
    if not df_limpio["presupuesto"].map(lambda x: 0 <= x < float("inf")).all():
        raise ValueError("Los presupuestos deben ser finitos y no negativos")
    if df_limpio["id"].duplicated().any():
        raise ValueError("IDs de leads duplicados")
    catalogo = pd.read_csv(os.path.join(os.path.dirname(DATA_IN), "desarrollos.csv"))
    invalidos = ~df_limpio["desarrollo_id"].isin(catalogo["id"])
    revision = df_limpio.loc[invalidos].copy()
    df_limpio = df_limpio.loc[~invalidos].reset_index(drop=True)
    df_limpio.attrs["revision"] = revision
    return df_limpio

def generar_resumen(df: pd.DataFrame):
    """
    3. Imprimir métricas en consola:
       - Total de prospectos limpios.
       - Cantidad de prospectos por origen.
       - Cantidad de prospectos por estatus normalizado.
    """
    print("\n--- RESUMEN DE LEADS ---")
    # Estos conteos describen los registros que se exportaran al CSV.
    print(f"Total de prospectos limpios: {len(df)}")
    print("\nProspectos por origen:")
    print(df["origen"].value_counts(dropna=False).to_string())
    print("\nProspectos por estatus normalizado:")
    print(df["estatus"].value_counts().reindex(
        ["NUEVO", "CONTACTADO", "EN_SEGUIMIENTO", "CONVERTIDO", "PERDIDO"],
        fill_value=0,
    ).to_string())

def exportar_datos(df: pd.DataFrame):
    """4. Guardar dataset limpio listo para base de datos."""
    df.to_csv(DATA_OUT, index=False)
    revision = df.attrs.get("revision", df.iloc[:0])
    revision.to_csv(os.path.join(os.path.dirname(DATA_OUT), "leads_revision.csv"), index=False)
    print(f"Prospectos separados para revisión de desarrollo: {len(revision)}")
    print(f"\nDataset limpio guardado en: {DATA_OUT}")

def enviar_muestra_api(df: pd.DataFrame, limite: int = 5, *, max_reintentos: int = 3):
    """Enviar una muestra; reintentar únicamente rechazos explícitos HTTP 429."""
    if isinstance(limite, bool) or not isinstance(limite, int) or limite < 0:
        raise ValueError("limite debe ser un entero mayor o igual a cero")
    if isinstance(max_reintentos, bool) or not isinstance(max_reintentos, int) or max_reintentos < 0:
        raise ValueError("max_reintentos debe ser un entero mayor o igual a cero")
    muestra = json.loads(df.head(limite).to_json(orient="records"))
    resultado = {"solicitados": len(muestra), "enviados": 0, "fallidos": []}
    url = os.getenv("CRM_API_URL", "http://127.0.0.1:8000/api/leads")
    token = os.getenv("CRM_API_TOKEN", "atlas-token-2026")
    for indice, lead in enumerate(muestra):
        lead["telefono"] = str(lead.get("telefono") or "")
        for intento in range(max_reintentos + 1):
            try:
                respuesta = requests.post(url, headers={"Authorization": f"Bearer {token}"}, json=lead, timeout=10)
                if respuesta.status_code == 401:
                    resultado["fallidos"].extend(item["id"] for item in muestra[indice:])
                    print("HTTP 401: revisa CRM_API_TOKEN; se detiene el envío.")
                    return resultado
                if respuesta.status_code == 429 and intento < max_reintentos:
                    retry_after = respuesta.headers.get("Retry-After", "")
                    try:
                        espera = float(retry_after)
                    except ValueError:
                        try:
                            espera = (parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds()
                        except (TypeError, ValueError, OverflowError):
                            espera = 2 ** intento
                    # No esperar menos que Retry-After: aplazar si supera el límite local.
                    if espera > 60 or not float("-inf") < espera < float("inf"):
                        respuesta.raise_for_status()
                    time.sleep(max(0, espera))
                    continue
                respuesta.raise_for_status()
            except requests.RequestException as error:
                resultado["fallidos"].append(lead["id"])
                print(f"No se pudo enviar el lead {lead['id']}: {error}")
            else:
                resultado["enviados"] += 1
                print(f"Lead {lead['id']} enviado (HTTP {respuesta.status_code}).")
            break
    print(f"Muestra API: {resultado['enviados']}/{len(muestra)} prospectos enviados.")
    return resultado


def main():
    parser = argparse.ArgumentParser(description="Limpieza de leads y sincronización con CRM")
    parser.add_argument("--enviar-api", action="store_true", help="Enviar la muestra al CRM local")
    parser.add_argument("--limite", type=int, default=5)
    args = parser.parse_args()
    if args.limite < 0:
        parser.error("--limite debe ser mayor o igual a cero")
    limpio = limpiar_datos(cargar_datos())
    generar_resumen(limpio)
    exportar_datos(limpio)
    if args.enviar_api:
        resultado = enviar_muestra_api(limpio, args.limite)
        return 1 if resultado["fallidos"] else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
