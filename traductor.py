from lark import Transformer
from estilos import convertir_a_css, TAG_CONTENEDOR, CLASE_CONTENEDOR

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
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }}

        /* Ventana raíz: ES la página, no una tarjeta dentro de ella */
        .ventana-raiz {{
            width: 100%;
            min-height: 100vh;
            padding: 25px;
        }}
        .titulo-raiz {{ margin-top: 0; }}

        /* Ventanas anidadas se ven como tarjetas */
        .ventana {{
            border: 1px solid #e5e7eb;
            padding: 20px;
            margin: 15px 0;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }}

        /* Contenedores de layout: sin estilo forzado, el DSL controla todo vía propiedades */
        .encabezado, .pie, .barra-lateral, .contenido-principal, .contenedor {{
            display: block;
        }}

        .texto {{ margin-bottom: 10px; color: #333; }}
        .parrafo {{ margin-bottom: 10px; color: #333; line-height: 1.5; }}
        .boton {{ background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; display: inline-block; }}
        .boton:hover {{ opacity: 0.9; }}
        .input-text {{ padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100%; margin-bottom: 10px; display: block; }}
        .textarea {{ padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100%; margin-bottom: 10px; display: block; font-family: inherit; }}
        .enlace {{ color: #007bff; text-decoration: none; display: inline-block; margin-bottom: 10px; }}
        .enlace:hover {{ text-decoration: underline; }}
        .separador {{ border: none; border-top: 1px solid #ddd; margin: 15px 0; }}
        .campo-check {{ margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
        .etiqueta {{ display: block; margin-bottom: 6px; font-weight: 600; color: #333; }}
        .select-campo {{ padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100%; margin-bottom: 10px; display: block; }}
        h1, h2, h3, h4, h5, h6 {{ margin: 10px 0; }}
    </style>
</head>
<body>
{contenido}
</body>
</html>"""

    def bloque_ventanas(self, args):
        return "\n".join(str(arg) for arg in args)

    def ventana_raiz(self, args):
        titulo = args[1].value.strip('"')
        propiedades = args[2] or {}
        elementos = args[4]
        style_inline = convertir_a_css(propiedades)
        return f'<div class="ventana-raiz" style="{style_inline}">\n  <h1 class="titulo-raiz">{titulo}</h1>\n  {elementos}\n</div>'

    def ventana(self, args):
        titulo = args[1].value.strip('"')
        propiedades = args[2] or {}
        elementos = args[4]
        style_inline = convertir_a_css(propiedades)
        return f'<div class="ventana" style="{style_inline}">\n  <h2>{titulo}</h2>\n  {elementos}\n</div>'

    def contenedor(self, args):
        tipo = args[0]                 # string, viene de tipo_contenedor
        propiedades = args[1] or {}
        elementos = args[3]

        tag = TAG_CONTENEDOR.get(tipo, "div")
        clase = CLASE_CONTENEDOR.get(tipo, "contenedor")
        style = convertir_a_css(propiedades)
        return f'<{tag} class="{clase}" style="{style}">\n  {elementos}\n</{tag}>'

    def tipo_contenedor(self, args):
        return args[0].value

    def lista_elementos(self, args):
        return "\n".join(str(arg) for arg in args)

    def elemento(self, args):
        return args[0]

    def contenido_opcional(self, args):
        if not args:
            return ""
        return args[0].value.strip('"')

    def componente_simple(self, args):
        tipo = args[0]
        contenido = args[1]
        propiedades = args[2] or {}

        style = convertir_a_css(propiedades)

        if tipo == "Texto":
            return f'<p class="texto" style="{style}">{contenido}</p>'
        elif tipo == "Parrafo":
            return f'<p class="parrafo" style="{style}">{contenido}</p>'
        elif tipo == "Input":
            return f'<input type="text" class="input-text" placeholder="{contenido}" style="{style}" />'
        elif tipo == "TextArea":
            return f'<textarea class="textarea" placeholder="{contenido}" style="{style}"></textarea>'
        elif tipo == "Boton":
            return f'<button class="boton" style="{style}">{contenido}</button>'
        elif tipo == "Imagen":
            return f'<img src="{contenido}" alt="Imagen" style="max-width: 100%; {style}" />'
        elif tipo == "Enlace":
            href = propiedades.get("href", "#")
            return f'<a href="{href}" class="enlace" style="{style}">{contenido}</a>'
        elif tipo == "Titulo":
            nivel = propiedades.get("nivel", "2")
            try:
                nivel = int(nivel)
                if nivel < 1 or nivel > 6:
                    nivel = 2
            except (ValueError, TypeError):
                nivel = 2
            return f'<h{nivel} style="{style}">{contenido}</h{nivel}>'
        elif tipo == "Separador":
            return f'<hr class="separador" style="{style}" />'
        elif tipo == "CheckBox":
            return (f'<div class="campo-check">'
                    f'<input type="checkbox" style="{style}" />'
                    f'<label>{contenido}</label>'
                    f'</div>')
        elif tipo == "Radio":
            grupo = propiedades.get("grupo", "radio-grupo")
            return (f'<div class="campo-check">'
                    f'<input type="radio" name="{grupo}" style="{style}" />'
                    f'<label>{contenido}</label>'
                    f'</div>')
        elif tipo == "Etiqueta":
            return f'<label class="etiqueta" style="{style}">{contenido}</label>'
        elif tipo == "Select":
            opciones_raw = propiedades.get("opciones", "")
            opciones = [o.strip() for o in opciones_raw.split(",") if o.strip()]
            options_html = "\n".join(f'    <option value="{o}">{o}</option>' for o in opciones)
            return f'<select class="select-campo" style="{style}">\n{options_html}\n  </select>'

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

