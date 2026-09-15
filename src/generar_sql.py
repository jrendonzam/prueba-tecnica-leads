"""Genera INSERTs MySQL reproducibles a partir del CSV limpio."""
from pathlib import Path
from decimal import Decimal
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def literal(valor):
    if pd.isna(valor):
        return "NULL"
    # Literales hexadecimales UTF-8: independientes de NO_BACKSLASH_ESCAPES.
    return "CONVERT(X'" + str(valor).encode("utf-8").hex() + "' USING utf8mb4)"


def generar_sql():
    desarrollos = pd.read_csv(ROOT / "data/desarrollos.csv", dtype=str)
    leads = pd.read_csv(ROOT / "data/leads_limpios.csv", dtype=str, keep_default_na=False)
    if not set(leads.desarrollo_id).issubset(set(desarrollos.id)):
        raise ValueError("Existen leads con desarrollos inexistentes")
    lineas = ["-- Datos generados por python -m src.generar_sql. Cargar en tablas vacías.", "SET NAMES utf8mb4;", "START TRANSACTION;"]
    for tabla, df in (("desarrollos", desarrollos), ("leads", leads)):
        columnas = ", ".join("`" + c + "`" for c in df.columns)
        for registro in df.to_dict(orient="records"):
            valores = []
            for columna, valor in registro.items():
                if columna in {"id", "desarrollo_id"}:
                    valores.append(str(int(valor)))
                elif columna == "presupuesto":
                    numero = Decimal(valor)
                    if not numero.is_finite() or numero < 0:
                        raise ValueError("Presupuesto inválido")
                    valores.append(format(numero.quantize(Decimal("0.01")), "f"))
                else:
                    valores.append(literal(valor))
            lineas.append(f"INSERT INTO {tabla} ({columnas}) VALUES ({', '.join(valores)});")
    lineas.append("COMMIT;")
    destino = ROOT / "sql/seed.sql"
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"SQL generado: {len(desarrollos)} desarrollos y {len(leads)} leads en {destino}")


if __name__ == "__main__":
    generar_sql()
