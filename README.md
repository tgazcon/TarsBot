# TARSbot

Trabajo práctico de Estructura de Datos. Sistema de recomendación y exploración de películas mediante una interfaz de terminal.

Permite buscar películas por título, explorar por género, consultar el top 10 mejor valoradas, encontrar películas relacionadas a partir de una que ya le gustó al usuario y ver el catálogo completo ordenado alfabéticamente.

## Versión 2: árbol binario de búsqueda

En esta versión el catálogo se guarda también en un **árbol binario de búsqueda** ([servicios/arbol.py](servicios/arbol.py)):

- **Clave de ordenamiento: el título** (sin distinguir mayúsculas). Elegimos el título porque es el dato que el usuario escribe para buscar una película (opciones 1 y 4) y porque es único dentro del catálogo. El rating y el año se repiten entre películas y no se usan para buscar.
- **Árbol equilibrado**: las películas se ordenan por título y se inserta siempre la del medio, así la altura queda en log n y la búsqueda no degrada a O(n).
- **Operaciones**: inserción, búsqueda y los recorridos inorder, preorder y postorder.
- **Uso en la app**:
  - Las opciones 1 (buscar) y 4 (relacionadas) buscan el título en el árbol en lugar de recorrer la lista.
  - La opción 5 lista el catálogo de la A a la Z con el recorrido inorder, que devuelve las películas ordenadas sin tener que ordenarlas.

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
6. Salir
```

## Estructura del proyecto

```
Tarsbot/
├── main.py                  # Punto de entrada, solo arranca la terminal
├── prueba_complejidad.py    # Comparación de tiempos: búsqueda secuencial vs árbol
├── modelos/
│   └── pelicula.py           # Clase Pelicula (dominio, solo datos)
├── servicios/
│   ├── arbol.py              # Árbol binario de búsqueda: inserción, búsqueda y recorridos
│   └── catalogo.py           # Lógica: cargar, buscar, filtrar, top, relacionadas, catálogo A-Z
├── ui/
│   └── terminal.py           # Menú e interacción por input()
├── tests/
│   └── test_arbol.py         # Pruebas automáticas del árbol
├── datos/
│   └── peliculas.json        # Catálogo con 30 películas
└── Docs/                     # Requerimientos, casos de uso, diagramas e informe de complejidad
```

Cada capa tiene una responsabilidad única:

- **modelos**: representa una película, sin lógica de negocio ni de carga de datos.
- **servicios**: contiene las estructuras de datos y las operaciones sobre el catálogo (búsqueda, filtros, ranking, relaciones).
- **ui**: maneja los menús y la entrada/salida por consola, delegando toda la lógica a `servicios`.

## Funcionalidades

1. **Buscar película**: ingresa un título y muestra título, director, año, género y valoración. Busca en el árbol.
2. **Explorar por género**: ingresa un género y lista las películas del catálogo que pertenecen a él.
3. **Top 10**: muestra las 10 películas con mayor valoración.
4. **Películas relacionadas**: a partir de un título (buscado en el árbol), lista otras películas del catálogo que comparten género o director.
5. **Catálogo completo (A-Z)**: lista todas las películas ordenadas por título usando el recorrido inorder del árbol.
6. **Salir**: termina el programa.

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

### Comparación de estrategias

```bash
python prueba_complejidad.py
```

Mide el tiempo de la búsqueda secuencial y de la búsqueda en el árbol con 100, 1.000 y 10.000 películas. El análisis está en [Docs/06- Prueba de complejidad.md](Docs/06-%20Prueba%20de%20complejidad.md).

### Pruebas manuales

Se probaron manualmente las opciones del menú ejecutando `python main.py`. Capturas de cada caso en [Docs/capturas](Docs/capturas):

- `op1.png` — Buscar película por título
- `op2.png` — Explorar por género
- `op3.png` — Top 10 películas
- `op4.png` — Películas relacionadas
