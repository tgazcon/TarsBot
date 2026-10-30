import json

from modelos.pelicula import Pelicula
from servicios.arbol import ArbolPeliculas, crear_arbol_equilibrado
from servicios.arbol_general import ArbolCategorias

def cargar(ruta: str) -> list[Pelicula]:
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return [Pelicula(**item) for item in datos]


def listar(peliculas: list[Pelicula]) -> list[Pelicula]:
    return peliculas


def buscar_por_titulo(peliculas: list[Pelicula], titulo: str) -> Pelicula | None:
    for pelicula in peliculas:
        if pelicula.titulo.lower() == titulo.lower():
            return pelicula
    return None


def filtrar_por_genero(peliculas: list[Pelicula], genero: str) -> list[Pelicula]:
    return [p for p in peliculas if p.genero.lower() == genero.lower()]


def top_valoradas(peliculas: list[Pelicula], cantidad: int = 10) -> list[Pelicula]:
    return sorted(peliculas, key=lambda p: p.valoracion, reverse=True)[:cantidad]


def relacionadas(peliculas: list[Pelicula], pelicula: Pelicula) -> list[Pelicula]:
    return [
        p for p in peliculas
        if p is not pelicula and (p.genero == pelicula.genero or p.director == pelicula.director)
    ]


def crear_arbol(peliculas: list[Pelicula]) -> ArbolPeliculas:
    return crear_arbol_equilibrado(peliculas)


def buscar_por_titulo_arbol(arbol: ArbolPeliculas, titulo: str) -> Pelicula | None:
    return arbol.buscar(titulo)


def listar_alfabetico(arbol: ArbolPeliculas) -> list[Pelicula]:
    return arbol.inorder()


def crear_arbol_categorias(peliculas: list[Pelicula]) -> ArbolCategorias:
    arbol = ArbolCategorias("Películas")

    ordenadas = sorted(
        peliculas,
        key=lambda p: (p.genero.lower(), p.subgenero.lower(), p.titulo.lower())
    )

    for pelicula in ordenadas:
        ruta = [pelicula.genero]
        if pelicula.subgenero:
            ruta.append(pelicula.subgenero)
        arbol.agregar_pelicula(pelicula, ruta)

    return arbol


def dibujar_categorias(arbol: ArbolCategorias) -> list[str]:
    return arbol.dibujar()


def peliculas_de_categoria(arbol: ArbolCategorias, nombre: str) -> tuple[list[str], list[Pelicula]] | None:
    camino = arbol.camino_a(nombre)

    if camino is None:
        return None

    return [nodo.nombre for nodo in camino], camino[-1].todas_las_peliculas()


def ubicar_pelicula(arbol: ArbolCategorias, titulo: str) -> tuple[Pelicula, list[str]] | None:
    return arbol.ubicar_pelicula(titulo)