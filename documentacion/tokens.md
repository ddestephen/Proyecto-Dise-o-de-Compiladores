# Definición de Tokens

A continuación se describen los tokens reconocidos por el analizador léxico del DSL para la generación de interfaces HTML/CSS.

---

# Palabras clave

Las palabras clave representan los componentes principales del lenguaje y poseen un significado reservado.

## VENTANA

**Descripción:** Define una ventana o contenedor principal.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `Ventana` |
| **Lexema** | `Ventana` |

---

## TEXTO

**Descripción:** Define un componente de texto.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `Texto` |
| **Lexema** | `Texto` |

---

## INPUT

**Descripción:** Define un campo de entrada de datos.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `Input` |
| **Lexema** | `Input` |

---

## BOTON

**Descripción:** Define un botón.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `Boton` |
| **Lexema** | `Boton` |

---

## IMAGEN

**Descripción:** Define un componente de imagen.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `Imagen` |
| **Lexema** | `Imagen` |

---

# Símbolos y delimitadores

Estos tokens permiten delimitar bloques y listas de propiedades.

## LKEY

**Descripción:** Inicio de un bloque.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `\{` |
| **Lexema** | `{` |

---

## RKEY

**Descripción:** Fin de un bloque.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `\}` |
| **Lexema** | `}` |

---

## LBRACKET

**Descripción:** Inicio de una lista de propiedades.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `\[` |
| **Lexema** | `[` |

---

## RBRACKET

**Descripción:** Fin de una lista de propiedades.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `\]` |
| **Lexema** | `]` |

---

## IGUAL

**Descripción:** Operador de asignación.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `=` |
| **Lexema** | `=` |

---

## COMA

**Descripción:** Separador de propiedades.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `,` |
| **Lexema** | `,` |

---

# Literales

Los literales representan valores constantes utilizados dentro del lenguaje.

## CADENA

**Descripción:** Secuencia de caracteres delimitada por comillas dobles.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `"[^"]*"` |
| **Ejemplos** | `"Hola"`, `"Mi aplicación"` |

---

## COLOR_HEX

**Descripción:** Color expresado en notación hexadecimal.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `#[0-9a-fA-F]{3,6}` |
| **Ejemplos** | `#000000`, `#FFFFFF`, `#1A84B5` |

---

## COLOR_RGB

**Descripción:** Color expresado mediante el modelo RGB.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `rgb\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)` |
| **Ejemplos** | `rgb(0,0,0)`, `rgb(255,255,255)` |

---

## NUMERO_CON_UNIDAD

**Descripción:** Número entero acompañado de una unidad de medida.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `\d+(px|%)` |
| **Ejemplos** | `250px`, `80%` |

---

## IDENTIFICADOR

**Descripción:** Nombre utilizado para representar propiedades o referencias.

| Atributo | Valor |
|----------|-------|
| **Patrón** | `[a-zA-Z_][a-zA-Z0-9_]*` |
| **Ejemplos** | `ancho`, `color`, `guardarDatos`, `tituloPrincipal` |