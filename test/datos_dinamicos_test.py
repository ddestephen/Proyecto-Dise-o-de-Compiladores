"""
datos_dinamicos.py

HU-02: Como desarrollador, quiero implementar expresiones regulares para
los tipos de datos dinámicos (cadenas, identificadores, colores HEX/RGB
y tamaños) para capturar sus valores.

Ejecutar:  python3 datos_dinamicos_test.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer_dsl import tokenize


class TiposDinamicos(unittest.TestCase):

    def test_cadena_simple(self):
        self.assertEqual(tokenize('"Mi app"'), [("CADENA", '"Mi app"')])

    def test_cadena_vacia(self):
        self.assertEqual(tokenize('""'), [("CADENA", '""')])

    def test_identificador_simple(self):
        for texto in ["click", "guardarDatos", "color2", "_privado"]:
            with self.subTest(texto=texto):
                self.assertEqual(tokenize(texto), [("IDENTIFICADOR", texto)])

    def test_color_hex_3_digitos(self):
        self.assertEqual(tokenize("#fff"), [("COLOR_HEX", "#fff")])

    def test_color_hex_6_digitos(self):
        for texto in ["#000000", "#1a84b5", "#c9a226"]:
            with self.subTest(texto=texto):
                self.assertEqual(tokenize(texto), [("COLOR_HEX", texto)])

    def test_color_rgb_sin_espacios(self):
        self.assertEqual(tokenize("rgb(0,0,0)"), [("COLOR_RGB", "rgb(0,0,0)")])

    def test_color_rgb_con_espacios(self):
        self.assertEqual(
            tokenize("rgb( 12 , 200 , 5 )"),
            [("COLOR_RGB", "rgb( 12 , 200 , 5 )")],
        )

    def test_numero_con_unidad_px(self):
        self.assertEqual(tokenize("890px"), [("NUMERO_CON_UNIDAD", "890px")])
        self.assertEqual(tokenize("0px"), [("NUMERO_CON_UNIDAD", "0px")])

    def test_numero_con_unidad_porcentaje(self):
        self.assertEqual(tokenize("18%"), [("NUMERO_CON_UNIDAD", "18%")])
        self.assertEqual(tokenize("100%"), [("NUMERO_CON_UNIDAD", "100%")])

    def test_propiedad_completa_con_varios_tipos_dinamicos(self):
        resultado = tokenize("color=azul, tamano=890px, fondo=#1a84b5, borde=rgb(2,1,3)")
        esperado = [
            ("IDENTIFICADOR", "color"), ("IGUAL", "="), ("IDENTIFICADOR", "azul"), ("COMA", ","),
            ("IDENTIFICADOR", "tamano"), ("IGUAL", "="), ("NUMERO_CON_UNIDAD", "890px"), ("COMA", ","),
            ("IDENTIFICADOR", "fondo"), ("IGUAL", "="), ("COLOR_HEX", "#1a84b5"), ("COMA", ","),
            ("IDENTIFICADOR", "borde"), ("IGUAL", "="), ("COLOR_RGB", "rgb(2,1,3)"),
        ]
        self.assertEqual(resultado, esperado)


if __name__ == "__main__":
    unittest.main(verbosity=2)