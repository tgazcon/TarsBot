# TARSbot

Trabajo práctico de Estructura de Datos. Sistema de recomendación y exploración de películas mediante una interfaz de terminal.

Permite buscar películas por título, explorar por género y por categorías, consultar el top 10 mejor valoradas, obtener recomendaciones a partir de una película que ya le gustó al usuario y recorrer la red de relaciones entre películas.

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
├── ejemplo_categorias.py    # Ejemplos de recorridos del árbol de categorías
├── modelos/
│   └── pelicula.py           # Clase Pelicula (dominio, solo datos)
├── servicios/
│   ├── arbol.py              # Árbol binario de búsqueda
│   ├── avl.py                # Árbol AVL
│   ├── arbol_general.py      # Árbol general de categorías
│   ├── heap.py               # Heap binaria de máximos
│   ├── grafo.py              # Grafo de películas: vecinos, BFS, DFS y camino más corto
│   └── catalogo.py           # Lógica: cargar, buscar, filtrar, rankings, categorías y red
├── ui/
│   └── terminal.py           # Menús e interacción por input()
├── tests/
│   ├── test_arbol.py
│   ├── test_avl.py
│   ├── test_arbol_general.py
│   ├── test_heap.py
│   └── test_grafo.py
├── datos/
│   └── peliculas.json        # Catálogo con 30 películas
└── Docs/                     # Requerimientos, casos de uso, diagramas e informes
```

Cada capa tiene una responsabilidad única:

- **modelos**: representa una película, sin lógica de negocio ni de carga de datos.
- **servicios**: contiene las estructuras de datos y las operaciones sobre el catálogo.
- **ui**: maneja los menús y la entrada/salida por consola, delegando toda la lógica a `servicios`.

## Funcionalidades

1. **Buscar película**: muestra los datos de una película a partir de su título. Busca en el árbol binario de búsqueda.
2. **Explorar por género**: lista las películas de un género.
3. **Top 10**: muestra las 10 películas con mayor valoración, obtenidas con la heap.
4. **Películas relacionadas**: a partir de una película, muestra un Top 5 de las que comparten género o director, ordenadas con la heap por un puntaje que combina valoración y parecido.
5. **Catálogo completo (A-Z)**: lista todas las películas ordenadas por título con el recorrido inorder del árbol.
6. **Explorar categorías**: submenú para ver el árbol de categorías (género y subgénero), las películas de una categoría o en qué categoría está una película. Usa el árbol general.
7. **Red de películas**: submenú para ver las conexiones de una película, el camino más corto entre dos, los grados de separación (BFS) y la exploración en profundidad (DFS). Usa el grafo.
8. **Salir**: termina el programa.

## Pruebas

### Pruebas automáticas

Desde la raíz del proyecto:

```bash
python -m unittest -v
```

Hay pruebas para cada estructura de datos: el árbol binario de búsqueda, el AVL, el árbol de categorías, la heap y el grafo (72 en total).

### Comparaciones

- `python prueba_complejidad.py`: búsqueda secuencial contra árbol. Informe en [Docs/05- Prueba de complejidad.md](Docs/05-%20Prueba%20de%20complejidad.md).
- `python prueba_avl.py`: BST contra AVL con datos desbalanceados. Informe en [Docs/06-AVL.md](Docs/06-AVL.md).
- `python ejemplo_categorias.py`: recorridos del árbol de categorías. Informe en [Docs/07-Arbol-de-categorias.md](Docs/07-Arbol-de-categorias.md).

### Pruebas manuales

Se probaron manualmente las opciones del menú ejecutando `python main.py`. Capturas en [Docs/capturas/BST](Docs/capturas/BST):

- `op1.png` — Buscar película por título
- `op2.png` — Explorar por género
- `op3.png` — Top 10 películas
- `op4.png` — Películas relacionadas
