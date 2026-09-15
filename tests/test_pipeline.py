import unittest
from unittest.mock import patch, Mock
import pandas as pd
import requests
from src.procesar_leads import cargar_datos, limpiar_datos, enviar_muestra_api


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.base = cargar_datos().head(1).copy()

    def response(self, code, headers=None):
        response = requests.Response()
        response.status_code = code
        response.headers.update(headers or {})
        return response

    def test_dataset_completo(self):
        original = cargar_datos()
        limpio = limpiar_datos(original)
        esperado = original.email.astype("string").str.strip().str.lower().dropna()
        self.assertEqual(len(limpio) + len(limpio.attrs["revision"]), esperado[esperado.ne("")].nunique())
        self.assertEqual(len(limpio.attrs["revision"]), 24)
        self.assertFalse(limpio.email.duplicated().any())
        self.assertTrue(limpio.fecha_registro.str.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$").all())
        self.assertTrue(limpio.presupuesto.notna().all())
        self.assertTrue(set(limpio.desarrollo_id) <= set(range(1, 7)))

    def test_limpieza_y_no_mutacion(self):
        df = pd.concat([self.base] * 3, ignore_index=True)
        df["email"] = [" A@B.COM ", "a@b.com", "  "]
        df["fecha_registro"] = "05/09/2026"
        df["estatus"] = " Cerrado Ganado "
        df["presupuesto"] = None
        original = df.copy(deep=True)
        limpio = limpiar_datos(df)
        self.assertEqual(len(limpio), 1)
        self.assertEqual(limpio.iloc[0].email, "a@b.com")
        self.assertEqual(limpio.iloc[0].fecha_registro, "2026-09-05 00:00:00")
        self.assertEqual(limpio.iloc[0].estatus, "CONVERTIDO")
        self.assertEqual(limpio.iloc[0].presupuesto, 0)
        pd.testing.assert_frame_equal(df, original)

    def test_estatus_desconocido(self):
        self.base["estatus"] = "OTRO"
        with self.assertRaises(ValueError):
            limpiar_datos(self.base)

    def test_fecha_invalida(self):
        self.base["fecha_registro"] = "31/02/2026"
        with self.assertRaises(ValueError):
            limpiar_datos(self.base)

    @patch("src.procesar_leads.time.sleep")
    @patch("src.procesar_leads.requests.post")
    def test_retry_429(self, post, sleep):
        post.side_effect = [self.response(429, {"Retry-After": "2"}), self.response(200)]
        resultado = enviar_muestra_api(limpiar_datos(self.base))
        self.assertEqual(resultado["enviados"], 1)
        sleep.assert_called_once_with(2)
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer atlas-token-2026")

    @patch("src.procesar_leads.requests.post")
    def test_401_detiene_lote(self, post):
        post.return_value = self.response(401)
        resultado = enviar_muestra_api(limpiar_datos(cargar_datos()).head(3))
        self.assertEqual(len(resultado["fallidos"]), 3)
        post.assert_called_once()

    @patch("src.procesar_leads.requests.post")
    def test_timeout_no_repite_post(self, post):
        post.side_effect = requests.Timeout("timeout")
        self.assertEqual(enviar_muestra_api(limpiar_datos(self.base))["enviados"], 0)
        post.assert_called_once()

    @patch("src.procesar_leads.time.sleep")
    @patch("src.procesar_leads.requests.post")
    def test_reintentos_acotados(self, post, sleep):
        post.return_value = self.response(429)
        self.assertEqual(len(enviar_muestra_api(limpiar_datos(self.base))["fallidos"]), 1)
        self.assertEqual(post.call_count, 4)


if __name__ == "__main__":
    unittest.main()
