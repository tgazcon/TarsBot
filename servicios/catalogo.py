import json

from modelos.pelicula import Pelicula
from servicios.arbol import ArbolPeliculas, crear_arbol_equilibrado
from servicios.arbol_general import ArbolCategorias
from servicios.grafo import GrafoPeliculas
from servicios.heap import MonticuloMaximo

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


def top_n(peliculas: list[Pelicula], cantidad: int, prioridad) -> list[tuple[float, Pelicula]]:
    """Las `cantidad` películas de mayor prioridad como (prioridad, película): heap en O(n) y `cantidad` extracciones en O(log n)."""
    monticulo = MonticuloMaximo.construir(peliculas, prioridad)
    resultado = []

    while len(resultado) < cantidad and not monticulo.esta_vacio():
        resultado.append(monticulo.extraer_maximo())

    return resultado


def top_valoradas(peliculas: list[Pelicula], cantidad: int = 10) -> list[Pelicula]:
    return [p for _, p in top_n(peliculas, cantidad, lambda p: p.valoracion)]


def relacionadas(peliculas: list[Pelicula], pelicula: Pelicula) -> list[Pelicula]:
    return [
        p for p in peliculas
        if p is not pelicula and (p.genero == pelicula.genero or p.director == pelicula.director)
    ]


# La valoración es la base y el parecido con la película elegida la sube
PESO_GENERO = 1.0
PESO_SUBGENERO = 0.5
PESO_DIRECTOR = 1.0


def afinidad(a: Pelicula, b: Pelicula) -> float:
    """Qué tan parecidas son dos películas: suma de lo que comparten (0 si no comparten nada)."""
    puntaje = 0.0

    if a.genero == b.genero:
        puntaje += PESO_GENERO

    if a.subgenero and a.subgenero == b.subgenero:
        puntaje += PESO_SUBGENERO

    if a.director == b.director:
        puntaje += PESO_DIRECTOR

    return puntaje


def puntaje_recomendacion(candidata: Pelicula, referencia: Pelicula) -> float:
    return round(candidata.valoracion + afinidad(candidata, referencia), 2)


def recomendar(peliculas: list[Pelicula], referencia: Pelicula, cantidad: int = 5) -> list[tuple[float, Pelicula]]:
    candidatas = relacionadas(peliculas, referencia)
    return top_n(candidatas, cantidad, lambda p: puntaje_recomendacion(p, referencia))


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


def crear_grafo(peliculas: list[Pelicula]) -> GrafoPeliculas:
    grafo = GrafoPeliculas()

    for pelicula in peliculas:
        grafo.agregar_vertice(pelicula)

    for i, a in enumerate(peliculas):
        for b in peliculas[i + 1:]:
            peso = afinidad(a, b)
            if peso > 0:
                grafo.agregar_arista(a, b, peso)

    return grafo


def conexiones_de(grafo: GrafoPeliculas, titulo: str) -> list[tuple[Pelicula, float]] | None:
    return grafo.vecinos(titulo)


def camino_entre(grafo: GrafoPeliculas, origen: str, destino: str) -> list[Pelicula] | None:
    return grafo.camino_mas_corto(origen, destino)


def dibujar_categorias(arbol: ArbolCategorias) -> list[str]:
    return arbol.dibujar()


def peliculas_de_categoria(arbol: ArbolCategorias, nombre: str) -> tuple[list[str], list[Pelicula]] | None:
    camino = arbol.camino_a(nombre)

    if camino is None:
        return None

    return [nodo.nombre for nodo in camino], camino[-1].todas_las_peliculas()


def ubicar_pelicula(arbol: ArbolCategorias, titulo: str) -> tuple[Pelicula, list[str]] | None:
    return arbol.ubicar_pelicula(titulo)