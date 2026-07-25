"""
test_lark.py

Prueba de reconocimiento de tokens

Ejecutar:  python3 lark_test.py
"""

import os

from lark import Lark
from lark.lexer import Token

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "gramatica_dsl.lark")


with open(GRAMMAR_PATH, encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(grammar, start="programa", parser="lalr", lexer="basic")

PROGRAMA_EJEMPLO = """
Ventana "Mi App" {
    Boton "Guardar" [color=azul, tamano=890px, fondo=#1a84b5, borde=rgb(2,1,3)]
    Input "Nombre"
    Texto "Bienvenido" [ancho=18%]
}
"""


def imprimir_tokens(texto: str):
    print("Tokens reconocidos:")
    print(f"{'TIPO':<20}{'LEXEMA'}")
    print("-" * 40)
    for tok in parser.lex(texto):  # type: Token
        print(f"{tok.type:<20}{tok.value}")


def probar_caso(nombre: str, texto: str):
    print(f"\n=== Caso: {nombre} ===")
    try:
        for tok in parser.lex(texto):
            print(f"  {tok.type:<18} -> {tok.value!r}")
        print("  OK: tokens reconocidos correctamente")
    except Exception as e:
        print(f"  ERROR: {e}")


if __name__ == "__main__":
    print("========== HU-01 y HU-02: programa de ejemplo completo ==========")
    imprimir_tokens(PROGRAMA_EJEMPLO)

    print("\n========== HU-01: palabras clave y símbolos ==========")
    probar_caso("Palabras clave", "Ventana Texto Input Boton Imagen")
    probar_caso("Símbolos", "{ } [ ] = ,")

    print("\n========== HU-02: tipos de datos dinámicos ==========")
    probar_caso("Cadena", '"Mi app"')
    probar_caso("Identificador", "click guardarDatos color2")
    probar_caso("Color HEX", "#000000 #1a84b5 #c9a226 #fff")
    probar_caso("Color RGB", "rgb(0,0,0) rgb(2, 1, 3) rgb( 12 , 200 , 5 )")
    probar_caso("Numero con unidad", "890px 18% 0px 100%")

    print("\nTodas las pruebas se ejecutaron.")