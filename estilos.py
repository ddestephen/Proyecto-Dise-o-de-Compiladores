# Diccionario de traducción de propiedades del DSL a propiedades CSS
MAPA_CSS = {
    "color": "color",
    "fondo": "background-color",
    "ancho": "width",
    "alto": "height",
    "padding": "padding",
    "margen": "margin",
    "tamano": "font-size",
    "alineacion": "text-align",
    "borde": "border",
    "radio": "border-radius",
    # ---- Flexbox / Grid ----
    "display": "display",
    "direccion": "flex-direction",
    "justificar": "justify-content",
    "alinear": "align-items",
    "espacio": "gap",
    "envolver": "flex-wrap",
    "flex": "flex",
    "orden": "order",
    "columnas": "grid-template-columns",
    "filas": "grid-template-rows",
    "columna": "grid-column",
    "fila": "grid-row",
    "posicion": "position",
}

# Propiedades especiales que NO deben convertirse a CSS (son atributos HTML o lógicos)
PROPS_NO_CSS = {"href", "nivel", "opciones", "placeholder", "checked", "for", "target", "grupo"}


def convertir_a_css(propiedades: dict) -> str:
    """Convierte un diccionario de propiedades del DSL a una cadena de estilos inline CSS,
    ignorando las que son atributos especiales (no CSS)."""
    if not propiedades:
        return ""
    estilos = []
    for clave, valor in propiedades.items():
        if clave.lower() in PROPS_NO_CSS:
            continue
        css_prop = MAPA_CSS.get(clave.lower(), clave.lower())
        estilos.append(f"{css_prop}: {valor};")
    return " ".join(estilos)

# Mapas de tipo de contenedor -> etiqueta HTML y clase CSS
TAG_CONTENEDOR = {
    "Header": "header",
    "Footer": "footer",
    "Aside": "aside",
    "Main": "main",
    "Contenedor": "div",
}
CLASE_CONTENEDOR = {
    "Header": "encabezado",
    "Footer": "pie",
    "Aside": "barra-lateral",
    "Main": "contenido-principal",
    "Contenedor": "contenedor",
}

