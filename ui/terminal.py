from pathlib import Path

from modelos.pelicula import Pelicula
from servicios import catalogo

RUTA_DATOS = Path(__file__).parent.parent / "datos" / "peliculas.json"


def mostrar_menu() -> None:
    print("\n===== TARSbot =====")
    print("1. Buscar película")
    print("2. Explorar por género")
    print("3. Top 10 películas")
    print("4. Películas relacionadas")
    print("5. Catálogo completo (A-Z)")
    print("6. Salir")


def mostrar_pelicula(pelicula: Pelicula) -> None:
    print(f"Título: {pelicula.titulo}")
    print(f"Director: {pelicula.director}")
    print(f"Año: {pelicula.estreno}")
    print(f"Género: {pelicula.genero}")
    print(f"Valoración: {pelicula.valoracion}")


def pedir_opcion() -> str:
    mostrar_menu()
    return input("Opción: ").strip()


def iniciar() -> None:
    peliculas = catalogo.cargar(RUTA_DATOS)
    arbol = catalogo.crear_arbol(peliculas)

    opcion = pedir_opcion()

    while opcion != "6":

        if opcion == "1":
            titulo = input("Ingrese el título: ")
            pelicula = catalogo.buscar_por_titulo_arbol(arbol, titulo)
            if pelicula:
                mostrar_pelicula(pelicula)
            else:
                print("No se encontró la película.")

        elif opcion == "2":
            genero = input("Ingrese el género: ")
            for p in catalogo.filtrar_por_genero(peliculas, genero):
                print(f"- {p.titulo}")

        elif opcion == "3":
            print("\n======== TOP 10 ========")
            for i, p in enumerate(catalogo.top_valoradas(peliculas), start=1):
                print(f"{i}. {p.titulo:<40} {p.valoracion}")

        elif opcion == "4":
            titulo = input("Ingrese el título: ")
            pelicula = catalogo.buscar_por_titulo_arbol(arbol, titulo)
            if pelicula:
                for p in catalogo.relacionadas(peliculas, pelicula):
                    print(f"- {p.titulo}")
            else:
                print("No se encontró la película.")

        elif opcion == "5":
            print("\n===== CATÁLOGO (A-Z) =====")
            for p in catalogo.listar_alfabetico(arbol):
                print(f"- {p.titulo:<52} {p.estreno}")

        else:
            print("Opción inválida.")

        opcion = pedir_opcion()

    print("Fin de TarsBot")
