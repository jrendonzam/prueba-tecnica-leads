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
    # TODO: Implementar lógica de limpieza
    return df_limpio

def generar_resumen(df: pd.DataFrame):
    """
    3. Imprimir métricas en consola:
       - Total de prospectos limpios.
       - Cantidad de prospectos por origen.
       - Cantidad de prospectos por estatus normalizado.
    """
    print("\n--- RESUMEN DE LEADS ---")
    # TODO: Mostrar conteos agregados
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
