import math
import random
import time

from modelos.pelicula import Pelicula
from servicios import catalogo
from servicios.arbol import ArbolPeliculas
from servicios.avl import ArbolAVL

RUTA_DATOS = "datos/peliculas.json"
REPETICIONES_BUSQUEDA = 200


def crear_peliculas(cantidad):
    return [
        Pelicula(f"Pelicula {i:05d}", "Director", 2020, "Accion", 7.0)
        for i in range(cantidad)
    ]


def construir(clase, peliculas):
    arbol = clase()
    inicio = time.perf_counter()
    for pelicula in peliculas:
        arbol.insertar(pelicula)
    return arbol, time.perf_counter() - inicio


def tiempo_busqueda(arbol, titulo):
    inicio = time.perf_counter()
    for _ in range(REPETICIONES_BUSQUEDA):
        arbol.buscar(titulo)
    return (time.perf_counter() - inicio) / REPETICIONES_BUSQUEDA


def comparar_orden(nombre, peliculas):
    titulo = peliculas[-1].titulo if nombre != "aleatorio" else peliculas[len(peliculas) // 2].titulo

    bst, t_bst = construir(ArbolPeliculas, peliculas)
    avl, t_avl = construir(ArbolAVL, peliculas)

    print(f"  {len(peliculas):>6}  {nombre:<11}"
          f"  {bst.altura():>7}  {avl.altura():>6}"
          f"  {t_bst:>9.4f}  {t_avl:>9.4f}"
          f"  {tiempo_busqueda(bst, titulo) * 1e6:>10.2f}"
          f"  {tiempo_busqueda(avl, titulo) * 1e6:>10.2f}"
          f"  {avl.rotaciones:>10}")


def experimento_sintetico():
    print("\n1) Títulos sintéticos insertados en distinto orden")
    print(f"  {'n':>6}  {'orden':<11}  {'alt BST':>7}  {'alt AVL':>6}"
          f"  {'build BST':>9}  {'build AVL':>9}"
          f"  {'busq BST us':>11}  {'busq AVL us':>11}  {'rotaciones':>10}")

    for cantidad in (100, 1000, 5000):
        peliculas = crear_peliculas(cantidad)

        mezcladas = peliculas[:]
        random.Random(42).shuffle(mezcladas)

        comparar_orden("ascendente", peliculas)
        comparar_orden("descendente", peliculas[::-1])
        comparar_orden("aleatorio", mezcladas)

    print("  (build = segundos para insertar todo; busq = microsegundos por búsqueda;"
          " ascendente/descendente buscan el último insertado)")


def experimento_catalogo():
    print("\n2) Catálogo real (30 películas) insertado en orden alfabético")

    peliculas = sorted(catalogo.cargar(RUTA_DATOS), key=lambda p: p.titulo.lower())

    bst, _ = construir(ArbolPeliculas, peliculas)
    avl, _ = construir(ArbolAVL, peliculas)
    ideal = math.ceil(math.log2(len(peliculas) + 1))

    print(f"  BST: altura {bst.altura()} (pasos máximos para buscar: {bst.altura()})")
    print(f"  AVL: altura {avl.altura()} (rotaciones hechas: {avl.rotaciones})")
    print(f"  Altura mínima posible para {len(peliculas)} nodos: {ideal}")


def main():
    experimento_sintetico()
    experimento_catalogo()


if __name__ == "__main__":
    main()
