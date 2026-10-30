# Organizá tu universo: árbol general de categorías

## Por qué un árbol general

Las películas tienen una jerarquía natural: una película pertenece a un subgénero (Cyberpunk), que es parte de un género (Ciencia ficción), que es parte del catálogo completo. Esa relación "es parte de" es un árbol, pero no uno binario: Ciencia ficción tiene tres subgéneros, Acción ninguno y Drama cinco. Cada categoría puede tener cualquier cantidad de hijos, y por eso se usa un **árbol general (n-ario)** ([servicios/arbol_general.py](../servicios/arbol_general.py)).

El árbol binario de búsqueda de la versión 2 y este árbol responden preguntas distintas. El BST ordena por título y sirve para encontrar una película rápido. El árbol de categorías agrupa y sirve para explorar: "¿qué hay en Drama?" o "¿dónde está Parasite?".

## La jerarquía

La jerarquía es `Películas → género → subgénero`. Cada película tiene un campo opcional `subgenero` en [datos/peliculas.json](../datos/peliculas.json), y el árbol se arma a partir de esos datos. Los números entre paréntesis son las películas que hay en cada categoría, contando las de sus subcategorías.

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

Acción, Animación y Fantasía no tienen subgéneros y guardan sus películas directamente, como Acción y Comedia en el ejemplo de la consigna. Por eso los nodos pueden tener subcategorías, películas o ambas cosas.

## Representación

- `NodoCategoria`: tiene un `nombre`, una lista de `hijos` (subcategorías) y una lista de `peliculas` propias.
- `ArbolCategorias`: guarda la raíz y las operaciones.

La lista de hijos es lo que permite tener cualquier cantidad de ramas en cada nodo, en lugar de los dos punteros (`izquierda` y `derecha`) del árbol binario.

## Operaciones

N es la cantidad de categorías y n la cantidad de películas.

| Operación | Qué hace | Costo |
|---|---|---|
| `agregar_pelicula(pelicula, ruta)` | Baja por la ruta (género, subgénero) creando las categorías que falten | O(h · k), con h la altura y k los hijos por nodo |
| `buscar_categoria(nombre)` | Busca una categoría en profundidad, sin distinguir mayúsculas | O(N) |
| `ruta_a(nombre)` | Camino de nombres desde la raíz hasta la categoría | O(N) |
| `ubicar_pelicula(titulo)` | Devuelve la película y la ruta de categorías donde está | O(N + n) |
| `todas_las_peliculas()` | Películas de una categoría y de todas sus subcategorías | O(N + n) del subárbol |
| `preorden`, `postorden`, `por_niveles` | Recorridos de todo el árbol | O(N) |
| `altura()` y `dibujar()` | Altura y dibujo del árbol | O(N) y O(N · n) |

Con 17 categorías y 30 películas todas las operaciones son instantáneas. `dibujar` recalcula la cantidad de películas de cada categoría, que es lo que lo hace O(N · n); no importa a este tamaño.

## Recorridos

Un árbol general no tiene "inorder", porque no hay una izquierda y una derecha entre las que poner al nodo. Se usan tres recorridos:

- **Preorden**: primero la categoría y después cada una de sus subcategorías. Es el orden en que se dibuja el árbol.
- **Postorden**: primero todas las subcategorías y después la categoría. Sirve cuando para resolver un nodo hay que tener resueltos sus hijos, como sumar las películas de una categoría.
- **Por niveles**: la raíz, después todas las categorías del nivel 1, después las del nivel 2, y así. Usa una cola en lugar de recursión.

Se obtienen con `python ejemplo_categorias.py`. Sobre el catálogo real dan:

```
Preorden (cada categoría antes que sus subcategorías)
 1. Películas (nivel 0)
 2. Acción (nivel 1)
 3. Animación (nivel 1)
 4. Ciencia ficción (nivel 1)
 5. Cyberpunk (nivel 2)
 6. Exploración espacial (nivel 2)
 7. Realidad y sueños (nivel 2)
 8. Drama (nivel 1)
 9. Carcelario (nivel 2)
10. Crimen (nivel 2)
11. Histórico (nivel 2)
12. Psicológico (nivel 2)
13. Social (nivel 2)
14. Fantasía (nivel 1)
15. Terror (nivel 1)
16. Sobrenatural (nivel 2)
17. Thriller psicológico (nivel 2)

Postorden (cada categoría después de sus subcategorías)
 1. Acción (nivel 1)
 2. Animación (nivel 1)
 3. Cyberpunk (nivel 2)
 4. Exploración espacial (nivel 2)
 5. Realidad y sueños (nivel 2)
 6. Ciencia ficción (nivel 1)
 7. Carcelario (nivel 2)
 8. Crimen (nivel 2)
 9. Histórico (nivel 2)
10. Psicológico (nivel 2)
11. Social (nivel 2)
12. Drama (nivel 1)
13. Fantasía (nivel 1)
14. Sobrenatural (nivel 2)
15. Thriller psicológico (nivel 2)
16. Terror (nivel 1)
17. Películas (nivel 0)

Por niveles (de la raíz hacia abajo)
 1. Películas (nivel 0)
 2. Acción (nivel 1)
 3. Animación (nivel 1)
 4. Ciencia ficción (nivel 1)
 5. Drama (nivel 1)
 6. Fantasía (nivel 1)
 7. Terror (nivel 1)
 8. Cyberpunk (nivel 2)
 9. Exploración espacial (nivel 2)
10. Realidad y sueños (nivel 2)
11. Carcelario (nivel 2)
12. Crimen (nivel 2)
13. Histórico (nivel 2)
14. Psicológico (nivel 2)
15. Social (nivel 2)
16. Sobrenatural (nivel 2)
17. Thriller psicológico (nivel 2)
```

Con el árbol de la consigna (Películas; Ciencia ficción con Cyberpunk, Viajes temporales e Inteligencia artificial; Acción; Comedia) los recorridos son:

| Recorrido | Orden de visita |
|---|---|
| Preorden | Películas, Ciencia ficción, Cyberpunk, Viajes temporales, Inteligencia artificial, Acción, Comedia |
| Postorden | Cyberpunk, Viajes temporales, Inteligencia artificial, Ciencia ficción, Acción, Comedia, Películas |
| Por niveles | Películas, Ciencia ficción, Acción, Comedia, Cyberpunk, Viajes temporales, Inteligencia artificial |

## Búsquedas

```
Ruta a 'Cyberpunk': Películas > Ciencia ficción > Cyberpunk
'Parasite' está en: Películas > Drama > Social
Categoría 'Western': None
```

`ubicar_pelicula` recorre el árbol entero, que es O(N + n). Si el catálogo fuera grande se podría buscar la película en el BST por título, que es O(log n), y armar la ruta con su género y su subgénero. Con 30 películas no hace falta.

## En la terminal

La opción 6 del menú, **Explorar categorías**, abre un submenú:

```
===== EXPLORAR CATEGORÍAS =====
1. Ver el árbol de categorías
2. Ver las películas de una categoría
3. ¿En qué categoría está una película?
4. Volver
```

La opción 2 acepta cualquier nivel de la jerarquía. Con un género devuelve también las películas de sus subgéneros:

```
Ingrese la categoría: cyberpunk

Películas > Ciencia ficción > Cyberpunk (2)
- Blade Runner 2049                                    2017
- The Matrix                                           1999
```

La opción 3 usa la búsqueda de películas del árbol:

```
Ingrese el título: The Matrix
The Matrix está en: Películas > Ciencia ficción > Cyberpunk
```

Las categorías y películas que no existen devuelven un mensaje ("No se encontró la categoría.") sin cortar el programa.

## Pruebas

```bash
python -m unittest -v
```

[tests/test_arbol_general.py](../tests/test_arbol_general.py) verifica los tres recorridos y la altura sobre el árbol de la consigna, las búsquedas de categorías y películas (con y sin resultado), que agregar una película reutiliza las categorías existentes y que el dibujo del árbol es el esperado. Con el catálogo real verifica que las 30 películas están en el árbol, que cada una queda en su género y subgénero, y que un género incluye las películas de sus subgéneros.
