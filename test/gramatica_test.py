"""
gramatica_test.py

HU-04: Como desarrollador, quiero codificar las reglas de producción en Lark
para estructurar el programa en componentes visuales.

hace diferentes pruebas de la gramatica definidad en el archivo .lark,
para verficar que la gramatica fue bien definida.


"""
import os
import unittest

from lark import Lark, Tree
from lark.exceptions import UnexpectedInput

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "gramatica_dsl.lark")

with open(GRAMMAR_PATH, encoding="utf-8") as f:
    GRAMMAR = f.read()

parser = Lark(GRAMMAR, start="programa", parser="lalr")


def _primer_elemento(arbol):
    """Atajo: navega programa -> bloque_ventanas -> ventana -> lista_elementos -> elemento."""
    ventana = arbol.children[0].children[0]
    lista_elementos = ventana.children[-2]
    return lista_elementos.children[0]


class EstructuraBasica(unittest.TestCase):
    """Checklist: las reglas de producción se integran y estructuran bien el programa."""

    def test_ventana_simple_sin_propiedades(self):
        arbol = parser.parse('Ventana "Mi App" { Input "Nombre" }')
        self.assertEqual(arbol.data, "programa")
        bloque = arbol.children[0]
        self.assertEqual(bloque.data, "bloque_ventanas")
        ventana = bloque.children[0]
        self.assertEqual(ventana.data, "ventana")
        lista_elementos = ventana.children[-2]
        self.assertEqual(lista_elementos.data, "lista_elementos")

    def test_componente_sin_propiedades_usa_la_rama_vacia(self):
        arbol = parser.parse('Ventana "App" { Boton "Guardar" }')
        elemento = _primer_elemento(arbol)
        componente = elemento.children[0]
        self.assertEqual(componente.data, "componente_simple")
        opcional_propiedades = componente.children[-1]
        # Rama vacía de "opcional_propiedades: LBRACKET lista_propiedades RBRACKET |"
        self.assertEqual(len(opcional_propiedades.children), 0)

    def test_componente_con_varias_propiedades_de_distinto_tipo(self):
        codigo = '''
        Ventana "App" {
            Boton "Guardar" [color=azul, tamano=890px, fondo=#1a84b5, borde=rgb(2,1,3)]
        }
        '''
        arbol = parser.parse(codigo)
        elemento = _primer_elemento(arbol)
        componente = elemento.children[0]
        lista_propiedades = componente.children[-1].children[1]  # [ lista_propiedades ]
        propiedades = [c for c in lista_propiedades.children if isinstance(c, Tree) and c.data == "propiedad"]
        self.assertEqual(len(propiedades), 4)

    def test_ventana_anidada_dentro_de_otra(self):
        codigo = '''
        Ventana "Principal" {
            Ventana "Secundaria" {
                Texto "Hola"
            }
        }
        '''
        arbol = parser.parse(codigo)
        elemento = _primer_elemento(arbol)
        # elemento: componente_simple | ventana  -> acá debe tomar la rama "ventana"
        ventana_interna = elemento.children[0]
        self.assertEqual(ventana_interna.data, "ventana")

    def test_varias_ventanas_al_mismo_nivel(self):
        codigo = '''
        Ventana "Uno" { Input "a" }
        Ventana "Dos" { Input "b" }
        '''
        arbol = parser.parse(codigo)
        bloque = arbol.children[0]
        self.assertEqual(len(bloque.children), 2)


class ErroresDeSintaxis(unittest.TestCase):
    """El parser debe rechazar programas que no respetan las reglas de producción."""

    def test_ventana_sin_ningun_elemento_dentro_falla(self):
        # "lista_elementos: elemento+" exige al menos un elemento
        with self.assertRaises(UnexpectedInput):
            parser.parse('Ventana "Vacia" { }')

    def test_falta_llave_de_cierre(self):
        with self.assertRaises(UnexpectedInput):
            parser.parse('Ventana "Mi App" { Input "Nombre"')

    def test_falta_cadena_del_titulo(self):
        with self.assertRaises(UnexpectedInput):
            parser.parse('Ventana { Input "Nombre" }')

    def test_propiedad_sin_valor(self):
        with self.assertRaises(UnexpectedInput):
            parser.parse('Ventana "App" { Boton "Guardar" [color=] }')

    def test_tipo_de_elemento_no_reconocido(self):
        # "Otro" no es TEXTO | INPUT | BOTON | IMAGEN, y tampoco es VENTANA
        with self.assertRaises(UnexpectedInput):
            parser.parse('Ventana "App" { Otro "Cosa" }')


if __name__ == "__main__":
    unittest.main(verbosity=2)
