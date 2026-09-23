# TARSbot

Trabajo práctico de Estructura de Datos. Sistema de recomendación y exploración de películas mediante una interfaz de terminal.

Permite buscar películas por título, explorar por género, consultar el top 10 mejor valoradas y encontrar películas relacionadas a partir de una que ya le gustó al usuario.

## Requisitos

- Python 3.9 o superior (se desarrolló con Python 3.13)

No requiere librerías externas.

## Ejecución

Desde la raíz del proyecto:

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
5. Salir
```

## Estructura del proyecto

```
Tarsbot/
├── main.py              # Punto de entrada, solo arranca la terminal
├── modelos/
│   └── pelicula.py       # Clase Pelicula (dominio, solo datos)
├── servicios/
│   └── catalogo.py       # Lógica: cargar, buscar, filtrar, listar, top, relacionadas
├── ui/
│   └── terminal.py       # Menú e interacción por input()
├── datos/
│   └── peliculas.json    # Catálogo con 30 películas
└── Docs/                 # Requerimientos, casos de uso y diagramas
```

Cada capa tiene una responsabilidad única:

- **modelos**: representa una película, sin lógica de negocio ni de carga de datos.
- **servicios**: contiene las operaciones sobre el catálogo (búsqueda, filtros, ranking, relaciones).
- **ui**: maneja los menús y la entrada/salida por consola, delegando toda la lógica a `servicios`.

## Funcionalidades

1. **Buscar película**: ingresa un título y muestra título, director, año, género y valoración.
2. **Explorar por género**: ingresa un género y lista las películas del catálogo que pertenecen a él.
3. **Top 10**: muestra las 10 películas con mayor valoración.
4. **Películas relacionadas**: a partir de un título, lista otras películas del catálogo que comparten género o director.
5. **Salir**: termina el programa.

## Pruebas

Se probaron manualmente las cuatro opciones del menú ejecutando `python main.py`. Capturas de cada caso en [Docs/capturas](Docs/capturas):

- `op1.png` — Buscar película por título
- `op2.png` — Explorar por género
- `op3.png` — Top 10 películas
- `op4.png` — Películas relacionadas
