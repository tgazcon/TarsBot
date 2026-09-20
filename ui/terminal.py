from modelos.pelicula import Pelicula
from servicios import catalogo

RUTA_DATOS = "datos/peliculas.json"


def mostrar_menu() -> None:
    print("\n===== TARSbot =====")
    print("1. Buscar película")
    print("2. Explorar por género")
    print("3. Top 10 películas")
    print("4. Películas relacionadas")
    print("5. Salir")


def mostrar_pelicula(pelicula: Pelicula) -> None:
    print(f"Título: {pelicula.titulo}")
    print(f"Director: {pelicula.director}")
    print(f"Año: {pelicula.estreno}")
    print(f"Género: {pelicula.genero}")
    print(f"Valoración: {pelicula.valoracion}")


def iniciar() -> None:
    peliculas = catalogo.cargar(RUTA_DATOS)

    mostrar_menu()
    opcion = int(input("Opción: "))
    
    while opcion!= 5:

        if opcion == 1:
            titulo = input("Ingrese el título: ")
            pelicula = catalogo.buscar_por_titulo(peliculas, titulo)
            if pelicula:
                mostrar_pelicula(pelicula)
            else:
                print("No se encontró la película.")

        elif opcion == 2:
            genero = input("Ingrese el género: ")
            for p in catalogo.filtrar_por_genero(peliculas, genero):
                print(f"- {p.titulo}")

        elif opcion == 3:
            print("\n======== TOP 10 ========")
            for i, p in enumerate(catalogo.top_valoradas(peliculas), start=1):
                print(f"{i}. {p.titulo:<40} {p.valoracion}")

        elif opcion == 4:
            titulo = input("Ingrese el título: ")
            pelicula = catalogo.buscar_por_titulo(peliculas, titulo)
            if pelicula:
                for p in catalogo.relacionadas(peliculas, pelicula):
                    print(f"- {p.titulo}")
            else:
                print("No se encontró la película.")

        elif opcion == 5:
            print("Fin de TarsBot")

        else:
            print("Opción inválida.")

        mostrar_menu()
        opcion = int(input("Opción: "))