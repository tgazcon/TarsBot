import time

from modelos.pelicula import Pelicula
from servicios import catalogo


def crear_peliculas(cantidad):
    peliculas = []

    for i in range(cantidad):
        pelicula = Pelicula(
            titulo="Pelicula " + str(i),
            director="Director",
            estreno=2020,
            genero="Accion",
            valoracion=7.0
        )

        peliculas.append(pelicula)

    return peliculas


def medir_secuencial(peliculas, titulo):
    inicio = time.perf_counter()

    catalogo.buscar_por_titulo(peliculas, titulo)

    fin = time.perf_counter()

    return fin - inicio


def medir_arbol(arbol, titulo):
    inicio = time.perf_counter()

    catalogo.buscar_por_titulo_arbol(arbol, titulo)

    fin = time.perf_counter()

    return fin - inicio


def probar(cantidad):
    print("\nCantidad de peliculas:", cantidad)

    peliculas = crear_peliculas(cantidad)

    arbol = catalogo.crear_arbol(peliculas)

    titulo = "Pelicula " + str(cantidad - 1)

    tiempo_secuencial = medir_secuencial(
        peliculas,
        titulo
    )

    tiempo_arbol = medir_arbol(
        arbol,
        titulo
    )

    print("Busqueda secuencial:", tiempo_secuencial)
    print("Busqueda en arbol:", tiempo_arbol)


def main():
    probar(100)
    probar(1000)
    probar(10000)


main()
