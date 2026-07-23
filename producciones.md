# Gramática del DSL

## Programa

```text
programa ::= bloque_ventanas
```

## Ventanas

```text
bloque_ventanas ::=
      ventana bloque_ventanas
    | ventana

ventana ::=
      VENTANA CADENA opcional_propiedades
      LKEY lista_elementos RKEY
```

## Elementos

```text
lista_elementos ::=
      elemento lista_elementos
    | elemento

elemento ::=
      componente_simple
    | ventana

componente_simple ::=
      tipo_elemento CADENA opcional_propiedades

tipo_elemento ::=
      TEXTO
    | INPUT
    | BOTON
    | IMAGEN
```

## Propiedades

```text
opcional_propiedades ::=
      LBRACKET lista_propiedades RBRACKET
    | ε

lista_propiedades ::=
      propiedad COMA lista_propiedades
    | propiedad

propiedad ::=
      IDENTIFICADOR IGUAL valor

valor ::=
      CADENA
    | IDENTIFICADOR
    | NUMERO_CON_UNIDAD
    | COLOR_HEX
    | COLOR_RGB
```