# Definicion inicial de tokens

A continuacion se definen los tokens que podran ser identificados por el lexer para un compilador de HTML/CSS.

## Palabras clave

#### VENTANA

**Patrón:** Ventana

**Lexema:** Ventana

#### TEXTO

+ **Patrón:** Texto

+ **Lexema:** Texto

#### INPUT

+ **Patrón:** Input

+ **Lexema:** Input

#### BOTON

+ **Patrón:** Boton

+ **Lexema:** Boton

#### IMAGEN

+ **Patrón:** Imagen

+ **Lexema:** Imagen

## Símbolos y delimitadores

#### LKEY

+ **Patrón:** \\{

+ **Lexema:** \{

#### RKEY

+ **Patrón:** \\}

+ **Lexema:** \}

#### LBRACKET

+ **Patrón:** \\[

+ **Lexema:** \[

#### RBRACKET

+ **Patrón:** \\]

+ **Lexema:** \]

#### IGUAL

+ **Patrón:** \=

+ **Lexema:** \=

#### COMA

+ **Patrón:** \,

+ **Lexema:** \,

## Literales

#### CADENA

+ **Patrón:** ¨[^¨]*¨

+ **Lexema:** Ejemplos: ¨hola¨, ¨Mi app¨

#### COLOR_HEX

+ **Patrón:** #[0-9a-fA-F]{3,6}

+ **Lexema:** Ejemplos: #000000, #1a84b5, #c9a226

#### COLOR_RGB

+ **Patrón:** rgb\s*\\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)

+ **Lexema:** Ejemplos: rgb(0,0,0), rgb(2,1,3)

#### NUMERO_CON_UNIDAD

+ **Patrón:** \d+(px|%)

+ **Lexema:** Ejemplos: 890px, 18%


#### IDENTIFICADOR

+ **Patrón:** [a-zA-Z_][a-zA-Z0-9_]*

+ **Lexema:**