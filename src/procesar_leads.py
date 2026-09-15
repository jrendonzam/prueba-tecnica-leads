"""
Módulo de Procesamiento y Limpieza de Leads
Completa las funciones indicadas para limpiar, validar y generar métricas del dataset.
"""
import os
import pandas as pd
import requests

DATA_IN = os.path.join(os.path.dirname(__file__), "..", "data", "leads.csv")
DATA_OUT = os.path.join(os.path.dirname(__file__), "..", "data", "leads_limpios.csv")

def cargar_datos() -> pd.DataFrame:
    """1. Cargar el dataset crudo."""
    df = pd.read_csv(DATA_IN)
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
    df_limpio = df.copy()

    # Eliminar registros con email vacío
    df_limpio["email"] = df_limpio["email"].fillna("").str.strip()
    df_limpio = df_limpio[df_limpio["email"] != ""]

    # Eliminar registros duplicados considerando el email
    df_limpio = df_limpio.drop_duplicates(subset="email")

    # Normalizar la columna estatus
    mapa_estatus = {
        "nuevo": "NUEVO",
        "contactado": "CONTACTADO",
        "en seguimiento": "EN_SEGUIMIENTO",
        "seguimiento": "EN_SEGUIMIENTO",
        "convertido": "CONVERTIDO",
        "cerrado ganado": "CONVERTIDO",
        "perdido": "PERDIDO",
        "descartado": "PERDIDO",
        "no interesado": "PERDIDO"
    }

    df_limpio["estatus"] = (
        df_limpio["estatus"]
        .fillna("")
        .str.strip()
        .str.lower()
        .map(mapa_estatus)
    )

    # Rellenar valores nulos de presupuesto con 0
    df_limpio["presupuesto"] = df_limpio["presupuesto"].fillna(0)

    return df_limpio


def generar_resumen(df: pd.DataFrame):
    """
    3. Imprimir métricas en consola:
       - Total de prospectos limpios.
       - Cantidad de prospectos por origen.
       - Cantidad de prospectos por estatus normalizado.
    """
    print("\n--- RESUMEN DE LEADS ---")

    print(f"Total de prospectos limpios: {len(df)}")

    print("\nProspectos por origen:")
    print(df["origen"].value_counts())

    print("\nProspectos por estatus:")
    print(df["estatus"].value_counts())

    pass

def exportar_datos(df: pd.DataFrame):
    """4. Guardar dataset limpio listo para base de datos."""
    df.to_csv(DATA_OUT, index=False)
    print(f"\nDataset limpio guardado en: {DATA_OUT}")

def enviar_muestra_api(df: pd.DataFrame, limite: int = 5):
    """
    5. Consumo de API:
       - Tomar una muestra de los primeros `limite` prospectos.
       - Enviar una petición POST a la API (http://127.0.0.1:8000/api/leads)
         utilizando el encabezado 'Authorization: Bearer atlas-token-2026'.
    """
    # TODO: Implementar llamada con la librería requests
    pass

if __name__ == "__main__":
    df = cargar_datos()
    df_limpio = limpiar_datos(df)
    generar_resumen(df_limpio)
    exportar_datos(df_limpio)
    # enviar_muestra_api(df_limpio)
