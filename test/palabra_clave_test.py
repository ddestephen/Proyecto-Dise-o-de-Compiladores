"""
palabras_clave_y_simbolos.py

HU-01: Como desarrollador, quiero definir los lexemas exactos para las
palabras reservadas (Ventana, Texto, Input, etc.) y símbolos (llaves,
corchetes, comas) para que el analizador léxico reconozca la estructura
básica.

Ejecutar:  python3 palabras_clave_y_simbolos.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer_dsl import tokenize


class PalabrasClave(unittest.TestCase):

    def test_reconoce_las_5_palabras_clave(self):
        resultado = tokenize("Ventana Texto Input Boton Imagen")
        esperado = [
            ("VENTANA", "Ventana"),
            ("TEXTO", "Texto"),
            ("INPUT", "Input"),
            ("BOTON", "Boton"),
            ("IMAGEN", "Imagen"),
        ]
        self.assertEqual(resultado, esperado)

    def test_palabra_clave_no_confunde_con_identificador_similar(self):
        # "Ventanas" (con 's') NO debe tokenizarse como VENTANA + algo raro,
        # debe ser un IDENTIFICADOR completo porque \b evita el corte a medias.
        resultado = tokenize("Ventanas")
        self.assertEqual(resultado, [("IDENTIFICADOR", "Ventanas")])

    def test_reconoce_llaves(self):
        self.assertEqual(tokenize("{"), [("LKEY", "{")])
        self.assertEqual(tokenize("}"), [("RKEY", "}")])

    def test_reconoce_corchetes(self):
        self.assertEqual(tokenize("["), [("LBRACKET", "[")])
        self.assertEqual(tokenize("]"), [("RBRACKET", "]")])

    def test_reconoce_igual_y_coma(self):
        self.assertEqual(tokenize("="), [("IGUAL", "=")])
        self.assertEqual(tokenize(","), [("COMA", ",")])

    def test_todos_los_simbolos_juntos(self):
        resultado = tokenize("{ } [ ] = ,")
        esperado = [
            ("LKEY", "{"), ("RKEY", "}"),
            ("LBRACKET", "["), ("RBRACKET", "]"),
            ("IGUAL", "="), ("COMA", ","),
        ]
        self.assertEqual(resultado, esperado)

    def test_estructura_basica_ventana_vacia(self):
        resultado = tokenize('Ventana "Mi App" { }')
        esperado = [
            ("VENTANA", "Ventana"),
            ("CADENA", '"Mi App"'),
            ("LKEY", "{"),
            ("RKEY", "}"),
        ]
        self.assertEqual(resultado, esperado)

    def test_espacios_en_blanco_se_ignoran(self):
        resultado = tokenize("Ventana    Texto\n\tInput")
        self.assertEqual(
            resultado,
            [("VENTANA", "Ventana"), ("TEXTO", "Texto"), ("INPUT", "Input")],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)