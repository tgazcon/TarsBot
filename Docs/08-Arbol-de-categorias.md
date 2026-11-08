
Las películas tienen una jerarquía natural: una película pertenece a un subgénero (Cyberpunk), que es parte de un género (Ciencia ficción), que es parte del catálogo completo. Ciencia ficción tiene tres subgéneros, Acción ninguno y Drama cinco. Cada categoría puede tener cualquier cantidad de hijos, y por eso se usa un árbol general (n-ario) ([servicios/arbol_general.py](../servicios/arbol_general.py)).

El BST ordena por título y sirve para encontrar una película rápido. El árbol de categorías agrupa y sirve para explorar: "¿qué hay en Drama?" o "¿dónde está Parasite?".

```
Películas (30)
├── Acción (4)
├── Animación (2)
├── Ciencia ficción (4)
│   ├── Cyberpunk (2)
│   ├── Exploración espacial (1)
│   └── Realidad y sueños (1)
├── Drama (14)
│   ├── Carcelario (2)
│   ├── Crimen (4)
│   ├── Histórico (2)
│   ├── Psicológico (4)
│   └── Social (2)
├── Fantasía (2)
└── Terror (4)
    ├── Sobrenatural (1)
    └── Thriller psicológico (3)
```


La lista de hijos es lo que permite tener cualquier cantidad de ramas en cada nodo, en lugar de los dos punteros (`izquierda` y `derecha`) del árbol binario.

## Recorridos

Un árbol general no tiene "inorder", porque no hay una izquierda y una derecha entre las que poner al nodo. Se usan tres recorridos:

- Preorden: primero la categoría y después cada una de sus subcategorías. Es el orden en que se dibuja el árbol.
- Postorden: primero todas las subcategorías y después la categoría. Sirve cuando para resolver un nodo hay que tener resueltos sus hijos, como sumar las películas de una categoría.
- Por niveles: la raíz, después todas las categorías del nivel 1, después las del nivel 2, y así. Usa una cola en lugar de recursión.

Se obtienen con `python ejemplo_categorias.py`. Sobre el catálogo real dan:

```
Preorden (cada categoría antes que sus subcategorías)

Postorden (cada categoría después de sus subcategorías)

Por niveles (de la raíz hacia abajo)

```


## En la terminal

La opción 6 del menú, Explorar categorías, abre un submenú:

```
===== EXPLORAR CATEGORÍAS =====
1. Ver el árbol de categorías
2. Ver las películas de una categoría
3. ¿En qué categoría está una película?
4. Volver
```

## Pruebas

```bash
python -m unittest -v
```

[tests/test_arbol_general.py](../tests/test_arbol_general.py) verifica los tres recorridos y la altura sobre el árbol de la consigna, las búsquedas de categorías y películas (con y sin resultado), que agregar una película reutiliza las categorías existentes y que el dibujo del árbol es el esperado. Con el catálogo real verifica que las 30 películas están en el árbol, que cada una queda en su género y subgénero, y que un género incluye las películas de sus subgéneros.
