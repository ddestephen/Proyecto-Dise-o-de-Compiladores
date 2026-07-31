import sys
from lark import Lark, Transformer

# 1. Cargar la gramática
with open("gramatica_dsl.lark", "r", encoding="utf-8") as f:
    gramatica = f.read()

parser = Lark(gramatica, start="programa", parser="lalr")

# Diccionario de traducción de propiedades del DSL a propiedades CSS
MAPA_CSS = {
    "color": "color",
    "fondo": "background-color",
    "ancho": "width",
    "alto": "height",
    "padding": "padding",
    "margen": "margin",
    "tamano": "font-size",
    "alineacion": "text-align"
}

def convertir_a_css(propiedades: dict) -> str:
    """Convierte un diccionario de propiedades del DSL a una cadena de estilos inline CSS."""
    if not propiedades:
        return ""
    estilos = []
    for clave, valor in propiedades.items():
        css_prop = MAPA_CSS.get(clave.lower(), clave.lower())
        estilos.append(f"{css_prop}: {valor};")
    return " ".join(estilos)


# 2. Transformer para convertir el AST en HTML/CSS
class GeneradorHTML(Transformer):
    def programa(self, args):
        contenido = args[0]
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interfaz Generada por DSL</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background-color: #f4f4f9; padding: 20px; }}
        .ventana {{ border: 1px solid #ccc; padding: 20px; margin: 15px 0; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .texto {{ margin-bottom: 10px; color: #333; }}
        .boton {{ background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; display: inline-block; }}
        .boton:hover {{ opacity: 0.9; }}
        .input-text {{ padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box; margin-bottom: 10px; display: block; }}
    </style>
</head>
<body>
{contenido}
</body>
</html>"""

    def bloque_ventanas(self, args):
        return "\n".join(str(arg) for arg in args)

    def ventana(self, args):
        titulo = args[1].value.strip('"')
        propiedades = args[2] or {}
        elementos = args[4]
        
        style_inline = convertir_a_css(propiedades)
        return f'<div class="ventana" style="{style_inline}">\n  <h2>{titulo}</h2>\n  {elementos}\n</div>'

    def lista_elementos(self, args):
        return "\n".join(str(arg) for arg in args)

    def elemento(self, args):
        return args[0]

    def componente_simple(self, args):
        tipo = args[0]
        contenido = args[1].value.strip('"')
        propiedades = args[2] or {}
        
        style = convertir_a_css(propiedades)

        if tipo == "Texto":
            return f'<p class="texto" style="{style}">{contenido}</p>'
        elif tipo == "Input":
            return f'<input type="text" class="input-text" placeholder="{contenido}" style="{style}" />'
        elif tipo == "Boton":
            return f'<button class="boton" style="{style}">{contenido}</button>'
        elif tipo == "Imagen":
            return f'<img src="{contenido}" alt="Imagen" style="max-width: 100%; {style}" />'
        return ""

    def tipo_elemento(self, args):
        return args[0].value

    def opcional_propiedades(self, args):
        if not args:
            return {}
        return args[1]

    def lista_propiedades(self, args):
        props = {}
        for arg in args:
            if isinstance(arg, dict):
                props.update(arg)
        return props

    def propiedad(self, args):
        clave = args[0].value
        valor = args[2]
        return {clave: valor}

    def valor(self, args):
        return args[0].value.strip('"')


# 3. Función principal
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
