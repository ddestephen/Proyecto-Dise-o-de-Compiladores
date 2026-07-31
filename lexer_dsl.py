"""
lexer_dsl.py

Módulo reutilizable que refleja EXACTAMENTE los patrones definidos en
gramatica_dsl.lark

"""
import re

# Orden de prioridad (igual al que aplicaría Lark):
# 1) palabras clave (coinciden como palabra completa con \b)
# 2) símbolos
# 3) tokens dinámicos (regex)

TOKEN_SPECS = [
    ("VENTANA", r"Ventana\b"),
    ("TEXTO", r"Texto\b"),
    ("INPUT", r"Input\b"),
    ("BOTON", r"Boton\b"),
    ("IMAGEN", r"Imagen\b"),
    ("LKEY", r"\{"),
    ("RKEY", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("IGUAL", r"="),
    ("COMA", r","),
    ("CADENA", r'"[^"]*"'),
    ("COLOR_HEX", r"#[0-9a-fA-F]{3,6}"),
    ("COLOR_RGB", r"rgb\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)"),
    ("NUMERO_CON_UNIDAD", r"\d+(?:px|%)"),
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("WS", r"[ \t\n\r]+"),
]

MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS)
)


class TokenNoReconocidoError(ValueError):
    """Se lanza cuando un carácter no coincide con ningún token definido."""

def tokenize(texto: str):
    """Convierte el texto en una lista de tuplas (tipo_token, lexema)."""
    pos = 0
    tokens = []
    while pos < len(texto):
        m = MASTER_RE.match(texto, pos)
        if not m:
            raise TokenNoReconocidoError(
                f"Carácter no reconocido en posición {pos}: {texto[pos]!r}"
            )
        kind = m.lastgroup
        value = m.group()
        if kind != "WS":
            tokens.append((kind, value))
        pos = m.end()
    return tokens