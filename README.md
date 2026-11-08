# TARSbot

Trabajo práctico de Estructura de Datos. Sistema de recomendación y exploración de películas mediante una interfaz de terminal.

Permite buscar películas por título, explorar por género, consultar el top 10 mejor valoradas, encontrar películas relacionadas a partir de una que ya le gustó al usuario, ver el catálogo completo ordenado alfabéticamente y explorar una jerarquía de categorías.

## Versión 2: árbol binario de búsqueda

En esta versión el catálogo se guarda también en un **árbol binario de búsqueda** ([servicios/arbol.py](servicios/arbol.py)):

- **Clave de ordenamiento: el título** (sin distinguir mayúsculas). Elegimos el título porque es el dato que el usuario escribe para buscar una película (opciones 1 y 4) y porque es único dentro del catálogo. El rating y el año se repiten entre películas y no se usan para buscar.
- **Árbol equilibrado**: las películas se ordenan por título y se inserta siempre la del medio, así la altura queda en log n y la búsqueda no degrada a O(n).
- **Operaciones**: inserción, búsqueda y los recorridos inorder, preorder y postorder.
- **Uso en la app**:
  - Las opciones 1 (buscar) y 4 (relacionadas) buscan el título en el árbol en lugar de recorrer la lista.
  - La opción 5 lista el catálogo de la A a la Z con el recorrido inorder, que devuelve las películas ordenadas sin tener que ordenarlas.

## Complemento: árbol AVL

El BST de la versión 2 solo está equilibrado porque se arma con cuidado; si los títulos llegan ordenados degenera en una lista (búsqueda O(n)). Se agregó un **árbol AVL** ([servicios/avl.py](servicios/avl.py)) que se reequilibra solo con rotaciones al insertar, y un experimento que compara ambos árboles con datos ordenados, desordenados y con el catálogo real. Con las 30 películas en orden alfabético el BST llega a altura 30 y el AVL a 5.

El análisis completo está en [Docs/07-AVL.md](Docs/07-AVL.md). El AVL es una pieza de estudio: la app sigue usando el BST equilibrado.

## Versión 3: árbol general de categorías

Las películas también se organizan en una **jerarquía natural del dominio** con un **árbol general (n-ario)** ([servicios/arbol_general.py](servicios/arbol_general.py)): cada categoría puede tener cualquier cantidad de subcategorías, a diferencia del árbol binario.

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

- **Jerarquía**: `Películas → género → subgénero`. Cada película tiene un campo opcional `subgenero` en `datos/peliculas.json`; los géneros que no lo usan (Acción, Animación, Fantasía) guardan sus películas directamente.
- **Operaciones**: agregar categorías y películas, buscar una categoría, obtener la ruta hasta ella, ubicar en qué categoría está una película, y los recorridos preorden, postorden y por niveles.
- **Uso en la app**: la opción 6 (Explorar categorías) muestra el árbol, lista las películas de una categoría (incluyendo las de sus subcategorías) y dice en qué categoría está una película.

Ejemplos de recorridos, decisiones de diseño y complejidad en [Docs/08-Arbol-de-categorias.md](Docs/08-Arbol-de-categorias.md).

## Versión 4: cola de prioridad (heap)

Los rankings del sistema se obtienen con una **heap binaria de máximos** implementada a mano ([servicios/heap.py](servicios/heap.py)):

- **Top 10** (opción 3): la prioridad es la valoración.
- **Recomendaciones** (opción 4): a partir de una película, muestra un Top 5 de las relacionadas. La prioridad combina la valoración con un bonus por parecido: mismo género (+1,0), mismo subgénero (+0,5) y mismo director (+1,0).
- **Top-N eficiente**: la heap se construye en O(n) y cada película pedida sale en O(log n), en total O(n + N log n), en lugar de ordenar todo el catálogo en cada consulta.

```
======== TOP 5 PARA INTERSTELLAR ========
1. Inception                                10.8
2. The Dark Knight                          10.0
3. The Matrix                               9.7
4. The Prestige                             9.5
5. Blade Runner 2049                        9.0
```

La función de prioridad y la justificación de por qué una heap y no ordenar están en [Docs/09-Cola-de-prioridad.md](Docs/09-Cola-de-prioridad.md).

## Versión 5: grafo de películas

Las relaciones entre películas se modelan como un **grafo** ([servicios/grafo.py](servicios/grafo.py)):

- **Vértice**: una película.
- **Arista**: dos películas conectadas si comparten género o director.
- **Peso**: la afinidad (+1,0 mismo género, +0,5 mismo subgénero, +1,0 mismo director).
- **Tipo**: no dirigido y pesado, porque el parecido es simétrico y no todas las relaciones valen lo mismo.
- **Representación**: lista de adyacencia, porque el grafo es poco denso (118 de 435 aristas posibles) y lo que más se consulta son los vecinos de una película.
- **Uso en la app**: la opción 7 (Red de películas) muestra las conexiones de una película, de la más fuerte a la más débil, y el camino más corto entre dos películas.

La justificación y ejemplos de consultas están en [Docs/10-Grafo.md](Docs/10-Grafo.md).

## Requisitos

- Python 3.10 o superior (se desarrolló con Python 3.13)

No requiere librerías externas.

## Ejecución

```bash
python main.py
```

Esto abre el menú interactivo en la terminal:

```
===== TARSbot =====
1. Buscar película
2. Explorar por género
3. Top 10 películas
4. Películas relacionadas
5. Catálogo completo (A-Z)
6. Explorar categorías
7. Red de películas
8. Salir
```

## Estructura del proyecto

```
Tarsbot/
├── main.py                  # Punto de entrada, solo arranca la terminal
├── prueba_complejidad.py    # Comparación de tiempos: búsqueda secuencial vs árbol
├── prueba_avl.py            # Experimentos de desbalance: BST común vs AVL
├── ejemplo_categorias.py    # Ejemplos de recorridos y búsquedas del árbol de categorías
├── modelos/
│   └── pelicula.py           # Clase Pelicula (dominio, solo datos)
├── servicios/
│   ├── arbol.py              # Árbol binario de búsqueda: inserción, búsqueda y recorridos
│   ├── avl.py                # Árbol AVL: inserción con rotaciones, búsqueda y recorridos
│   ├── arbol_general.py      # Árbol general de categorías: búsquedas, recorridos y dibujo
│   ├── heap.py               # Heap binaria de máximos: insertar, extraer y construir
│   ├── grafo.py              # Grafo de películas (lista de adyacencia): vecinos y camino más corto
│   └── catalogo.py           # Lógica: cargar, buscar, filtrar, top, relacionadas, catálogo A-Z, categorías
├── ui/
│   └── terminal.py           # Menú e interacción por input()
├── tests/
│   ├── test_arbol.py         # Pruebas automáticas del BST
│   ├── test_avl.py           # Pruebas automáticas del AVL
│   ├── test_arbol_general.py # Pruebas automáticas del árbol de categorías
│   ├── test_heap.py          # Pruebas automáticas de la heap y los rankings
│   └── test_grafo.py         # Pruebas automáticas del grafo
├── datos/
│   └── peliculas.json        # Catálogo con 30 películas
└── Docs/                     # Requerimientos, casos de uso, diagramas e informes (complejidad, AVL, categorías, heap y grafo)
```

Cada capa tiene una responsabilidad única:

- **modelos**: representa una película, sin lógica de negocio ni de carga de datos.
- **servicios**: contiene las estructuras de datos y las operaciones sobre el catálogo (búsqueda, filtros, ranking, relaciones).
- **ui**: maneja los menús y la entrada/salida por consola, delegando toda la lógica a `servicios`.

## Funcionalidades

1. **Buscar película**: ingresa un título y muestra título, director, año, género y valoración. Busca en el árbol.
2. **Explorar por género**: ingresa un género y lista las películas del catálogo que pertenecen a él.
3. **Top 10**: muestra las 10 películas con mayor valoración, obtenidas con la heap.
4. **Películas relacionadas**: a partir de un título (buscado en el árbol), muestra un Top 5 de las películas que comparten género o director, ordenadas por un puntaje que combina valoración y parecido.
5. **Catálogo completo (A-Z)**: lista todas las películas ordenadas por título usando el recorrido inorder del árbol.
6. **Explorar categorías**: abre un submenú para ver el árbol de categorías, listar las películas de una categoría (por ejemplo `Drama` o `Cyberpunk`) o saber en qué categoría está una película.
7. **Red de películas**: abre un submenú para ver las conexiones de una película (de la más fuerte a la más débil) o el camino más corto entre dos películas.
8. **Salir**: termina el programa.

## Pruebas

### Pruebas automáticas

Desde la raíz del proyecto:

```bash
python -m unittest -v
```

[tests/test_arbol.py](tests/test_arbol.py) verifica:

- Que con el ejemplo de la consigna (Matrix, Inception, Titanic) Matrix queda en la raíz, Inception a la izquierda y Titanic a la derecha.
- Los tres recorridos sobre ese árbol:
  - inorder: Inception, Matrix, Titanic
  - preorder: Matrix, Inception, Titanic
  - postorder: Inception, Titanic, Matrix
- La búsqueda en el catálogo real: una película que existe, una que no existe y sin distinguir mayúsculas.
- Que el árbol y la búsqueda secuencial devuelven la misma película para todos los títulos del catálogo.
- Que el catálogo A-Z tiene las 30 películas y está ordenado.
- El caso del árbol vacío.

[tests/test_avl.py](tests/test_avl.py) verifica las cuatro rotaciones del AVL, que queda balanceado al insertar en orden ascendente, descendente y aleatorio, y que con el catálogo real el BST llega a altura 30 y el AVL a 5.

[tests/test_arbol_general.py](tests/test_arbol_general.py) verifica:

- Los recorridos preorden, postorden y por niveles sobre el árbol de la consigna (Películas, Ciencia ficción con Cyberpunk, Viajes temporales e Inteligencia artificial, Acción y Comedia), y su altura.
- La búsqueda de categorías (sin distinguir mayúsculas), la ruta hasta una categoría y la ubicación de una película, incluyendo los casos que no existen.
- Que agregar una película crea las categorías que faltan y reutiliza las existentes.
- El dibujo del árbol con la cantidad de películas de cada categoría.
- Con el catálogo real: que cada película queda en su género y subgénero, que un género incluye las películas de sus subgéneros y que los géneros sin subgéneros guardan las películas directamente.

[tests/test_heap.py](tests/test_heap.py) verifica que la heap extrae de mayor a menor, el desempate por orden de entrada, que el Top 10 coincide con ordenar la lista y que el ranking de recomendaciones está ordenado y no incluye a la película elegida.

[tests/test_grafo.py](tests/test_grafo.py) verifica, con el grafo de ejemplo de la consigna, que es no dirigido y que el camino más corto funciona (incluyendo los casos sin camino), y con el catálogo real que el peso de las aristas es la afinidad.

### Comparación de estrategias

```bash
python prueba_complejidad.py
```

Mide el tiempo de la búsqueda secuencial y de la búsqueda en el árbol con 100, 1.000 y 10.000 películas. El análisis está en [Docs/06- Prueba de complejidad.md](Docs/06-%20Prueba%20de%20complejidad.md).

### Experimentos de desbalance

```bash
python prueba_avl.py
```

Compara altura, tiempo de armado y tiempo de búsqueda del BST común contra el AVL con 100, 1.000 y 5.000 películas. Resultados y conclusión en [Docs/07-AVL.md](Docs/07-AVL.md).

### Ejemplos de recorridos del árbol de categorías

```bash
python ejemplo_categorias.py
```

Muestra el árbol del catálogo real, los recorridos preorden, postorden y por niveles, y algunas búsquedas. La salida completa está en [Docs/08-Arbol-de-categorias.md](Docs/08-Arbol-de-categorias.md).

### Pruebas manuales

Se probaron manualmente las opciones del menú ejecutando `python main.py`. Capturas de cada caso en [Docs/capturas](Docs/capturas):

- `op1.png` — Buscar película por título
- `op2.png` — Explorar por género
- `op3.png` — Top 10 películas
- `op4.png` — Películas relacionadas
