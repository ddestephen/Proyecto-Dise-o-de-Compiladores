import sys
from lark import Lark
from traductor import GeneradorHTML

with open("gramatica_dsl.lark", "r", encoding="utf-8") as f:
    gramatica = f.read()

parser = Lark(gramatica, start="programa", parser="lalr")

def compilar(ruta_entrada: str, ruta_salida: str):
    try:
        with open(ruta_entrada, "r", encoding="utf-8") as f:
            codigo = f.read()

        arbol = parser.parse(codigo)
        generador = GeneradorHTML()
        html = generador.transform(arbol)

        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(html)

        print(f" Compilado con éxito: '{ruta_entrada}' -> '{ruta_salida}'")
    except Exception as e:
        print(f" Error de compilación: {e}")


if __name__ == "__main__":
    archivo_in = sys.argv[1] if len(sys.argv) > 1 else "prueba.txt"
    archivo_out = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    compilar(archivo_in, archivo_out)
