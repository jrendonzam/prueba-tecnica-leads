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

    # Estandarizar el correo antes de validar vacíos y duplicados.
    df_limpio["email"] = df_limpio["email"].astype("string").str.strip().str.lower()
    df_limpio = df_limpio[df_limpio["email"].notna() & df_limpio["email"].ne("")]
    df_limpio = df_limpio.drop_duplicates(subset="email", keep="first")

    # Quitar diferencias de mayúsculas, espacios y sinónimos del estatus.
    estatus_normalizado = (
        df_limpio["estatus"]
        .astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", "_", regex=True)
    )
    equivalencias_estatus = {
        "NUEVO": "NUEVO",
        "CONTACTADO": "CONTACTADO",
        "EN_SEGUIMIENTO": "EN_SEGUIMIENTO",
        "SEGUIMIENTO": "EN_SEGUIMIENTO",
        "CONVERTIDO": "CONVERTIDO",
        "CERRADO_GANADO": "CONVERTIDO",
        "PERDIDO": "PERDIDO",
        "DESCARTADO": "PERDIDO",
        "NO_INTERESADO": "PERDIDO",
    }
    df_limpio["estatus"] = estatus_normalizado.map(equivalencias_estatus)

    estatus_sin_equivalencia = df_limpio.loc[
        df_limpio["estatus"].isna(), "id"
    ].tolist()
    if estatus_sin_equivalencia:
        raise ValueError(
            "Hay estatus sin equivalencia en los registros con id: "
            f"{estatus_sin_equivalencia}"
        )

    # Convertir valores inválidos a nulos y sustituirlos por el promedio.
    df_limpio["presupuesto"] = pd.to_numeric(
        df_limpio["presupuesto"], errors="coerce"
    )
    presupuesto_promedio = df_limpio["presupuesto"].mean()
    df_limpio["presupuesto"] = df_limpio["presupuesto"].fillna(
        presupuesto_promedio if pd.notna(presupuesto_promedio) else 0
    )

    # Unificar las distintas representaciones de fecha para la exportación.
    fechas = pd.to_datetime(
        df_limpio["fecha_registro"],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )
    if fechas.isna().any():
        ids_fecha_invalida = df_limpio.loc[fechas.isna(), "id"].tolist()
        raise ValueError(
            "Hay fechas inválidas en los registros con id: "
            f"{ids_fecha_invalida}"
        )
    df_limpio["fecha_registro"] = fechas.dt.strftime("%Y-%m-%d %H:%M:%S")

    return df_limpio.reset_index(drop=True)


def generar_resumen(df: pd.DataFrame) -> None:
    """
    3. Imprimir métricas en consola:
       - Total de prospectos limpios.
       - Cantidad de prospectos por origen.
       - Cantidad de prospectos por estatus normalizado.
    """
    print("\n--- RESUMEN DE LEADS ---")
    print(f"Total de prospectos limpios: {len(df)}")

    print("\nProspectos por origen:")
    print(df["origen"].value_counts().to_string())

    print("\nProspectos por estatus:")
    print(df["estatus"].value_counts().to_string())


def exportar_datos(df: pd.DataFrame) -> None:
    """4. Guardar dataset limpio listo para base de datos."""
    df.to_csv(DATA_OUT, index=False)
    print(f"\nDataset limpio guardado en: {DATA_OUT}")


def enviar_muestra_api(df: pd.DataFrame, limite: int = 5) -> None:
    """
    5. Consumo de API:
       - Tomar una muestra de los primeros `limite` prospectos.
       - Enviar una petición POST a la API (http://127.0.0.1:8000/api/leads)
         utilizando el encabezado 'Authorization: Bearer atlas-token-2026'.
    """
    url = "http://127.0.0.1:8000/api/leads"
    headers = {"Authorization": "Bearer atlas-token-2026"}
    campos_api = [
        "id",
        "nombre",
        "email",
        "telefono",
        "origen",
        "fecha_registro",
        "estatus",
        "presupuesto",
        "desarrollo_id",
        "comentarios",
    ]

    muestra = df.head(limite)

    for _, fila in muestra.iterrows():
        payload = {
            campo: None if pd.isna(fila[campo]) else fila[campo]
            for campo in campos_api
        }
        #completado y corregido
        # Convertir tipos numéricos de pandas a tipos nativos serializables.
        payload["id"] = int(payload["id"])
        payload["desarrollo_id"] = int(payload["desarrollo_id"])
        payload["presupuesto"] = float(payload["presupuesto"])
        payload["telefono"] = (
            "N/A" if payload["telefono"] is None else str(payload["telefono"])
        )

        try:
            respuesta = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10,
            )
            if respuesta.ok:
                print(f"Lead {payload['id']} enviado: {respuesta.json()}")
            else:
                print(
                    f"Lead {payload['id']} rechazado "
                    f"({respuesta.status_code}): {respuesta.text}"
                )
        except requests.RequestException as error:
            print(f"No se pudo enviar el lead {payload['id']}: {error}")


if __name__ == "__main__":
    df = cargar_datos()
    df_limpio = limpiar_datos(df)
    generar_resumen(df_limpio)
    exportar_datos(df_limpio)
    enviar_muestra_api(df_limpio)
