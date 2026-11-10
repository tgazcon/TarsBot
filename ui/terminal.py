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
    print("6. Explorar categorías")
    print("7. Red de películas")
    print("8. Salir")


def mostrar_pelicula(pelicula: Pelicula) -> None:
    print(f"Título: {pelicula.titulo}")
    print(f"Director: {pelicula.director}")
    print(f"Año: {pelicula.estreno}")
    if pelicula.subgenero:
        print(f"Género: {pelicula.genero} / {pelicula.subgenero}")
    else:
        print(f"Género: {pelicula.genero}")
    print(f"Valoración: {pelicula.valoracion}")


def pedir_opcion() -> str:
    mostrar_menu()
    return input("Opción: ").strip()


def mostrar_menu_categorias() -> None:
    print("\n===== EXPLORAR CATEGORÍAS =====")
    print("1. Ver el árbol de categorías")
    print("2. Ver las películas de una categoría")
    print("3. ¿En qué categoría está una película?")
    print("4. Volver")


def explorar_categorias(arbol_categorias) -> None:
    mostrar_menu_categorias()
    opcion = input("Opción: ").strip()

    while opcion != "4":

        if opcion == "1":
            print()
            for linea in catalogo.dibujar_categorias(arbol_categorias):
                print(linea)

        elif opcion == "2":
            nombre = input("Ingrese la categoría: ")
            resultado = catalogo.peliculas_de_categoria(arbol_categorias, nombre)
            if resultado:
                ruta, peliculas = resultado
                print(f"\n{' > '.join(ruta)} ({len(peliculas)})")
                for p in peliculas:
                    print(f"- {p.titulo:<52} {p.estreno}")
            else:
                print("No se encontró la categoría.")

        elif opcion == "3":
            titulo = input("Ingrese el título: ")
            resultado = catalogo.ubicar_pelicula(arbol_categorias, titulo)
            if resultado:
                pelicula, ruta = resultado
                print(f"{pelicula.titulo} está en: {' > '.join(ruta)}")
            else:
                print("No se encontró la película.")

        else:
            print("Opción inválida.")

        mostrar_menu_categorias()
        opcion = input("Opción: ").strip()


def mostrar_menu_red() -> None:
    print("\n===== RED DE PELÍCULAS =====")
    print("1. Ver las conexiones de una película")
    print("2. Camino entre dos películas")
    print("3. Grados de separación (BFS)")
    print("4. Explorar en profundidad (DFS)")
    print("5. Volver")


def explorar_red(grafo) -> None:
    mostrar_menu_red()
    opcion = input("Opción: ").strip()

    while opcion != "5":

        if opcion == "1":
            titulo = input("Ingrese el título: ")
            conexiones = catalogo.conexiones_de(grafo, titulo)
            if conexiones is None:
                print("No se encontró la película.")
            else:
                print(f"\nConexiones de {grafo.buscar(titulo).titulo} ({len(conexiones)})")
                for p, peso in conexiones:
                    print(f"- {p.titulo:<52} {peso}")

        elif opcion == "2":
            origen = input("Película de origen: ")
            destino = input("Película de destino: ")
            if grafo.buscar(origen) is None or grafo.buscar(destino) is None:
                print("No se encontró alguna de las películas.")
            else:
                camino = catalogo.camino_entre(grafo, origen, destino)
                if camino is None:
                    print("No hay camino entre esas películas.")
                else:
                    print(" -> ".join(p.titulo for p in camino))
                    saltos = len(camino) - 1
                    print(f"({saltos} {'salto' if saltos == 1 else 'saltos'})")

        elif opcion == "3":
            titulo = input("Ingrese el título: ")
            niveles = catalogo.grados_de_separacion(grafo, titulo)
            if niveles is None:
                print("No se encontró la película.")
            elif not niveles:
                print(f"{grafo.buscar(titulo).titulo} no tiene ninguna película relacionada.")
            else:
                print(f"\nGrados de separación desde {grafo.buscar(titulo).titulo}")
                for distancia, peliculas_nivel in niveles:
                    print(f"\nA {distancia} {'salto' if distancia == 1 else 'saltos'} ({len(peliculas_nivel)}):")
                    for p in peliculas_nivel:
                        print(f"- {p.titulo}")

        elif opcion == "4":
            titulo = input("Ingrese el título: ")
            resultado = catalogo.explorar_en_profundidad(grafo, titulo)
            if resultado is None:
                print("No se encontró la película.")
            else:
                recorrido, no_alcanzadas = resultado
                print(f"\nExploración en profundidad desde {recorrido[0][0].titulo}\n")
                for p, profundidad in recorrido:
                    print(f"{'   ' * profundidad}{'└─ ' if profundidad else ''}{p.titulo}")
                alcanzadas = len(recorrido) - 1
                print(f"\nSe llega a {alcanzadas} {'película' if alcanzadas == 1 else 'películas'}.")
                if no_alcanzadas:
                    print(f"No se puede llegar a ({len(no_alcanzadas)}): {', '.join(p.titulo for p in no_alcanzadas)}")

        else:
            print("Opción inválida.")

        mostrar_menu_red()
        opcion = input("Opción: ").strip()


def iniciar() -> None:
    peliculas = catalogo.cargar(RUTA_DATOS)
    arbol = catalogo.crear_arbol(peliculas)
    arbol_categorias = catalogo.crear_arbol_categorias(peliculas)
    grafo = catalogo.crear_grafo(peliculas)

    opcion = pedir_opcion()

    while opcion != "8":

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
                print(f"\n======== TOP 5 PARA {pelicula.titulo.upper()} ========")
                for i, (puntaje, p) in enumerate(catalogo.recomendar(peliculas, pelicula), start=1):
                    print(f"{i}. {p.titulo:<40} {puntaje}")
            else:
                print("No se encontró la película.")

        elif opcion == "5":
            print("\n===== CATÁLOGO (A-Z) =====")
            for p in catalogo.listar_alfabetico(arbol):
                print(f"- {p.titulo:<52} {p.estreno}")

        elif opcion == "6":
            explorar_categorias(arbol_categorias)

        elif opcion == "7":
            explorar_red(grafo)

        else:
            print("Opción inválida.")

        opcion = pedir_opcion()

    print("Fin de TarsBot")
