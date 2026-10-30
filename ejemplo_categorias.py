from servicios import catalogo

RUTA_DATOS = "datos/peliculas.json"


def mostrar_recorrido(nombre, recorrido):
    print(f"\n{nombre}")
    for orden, (nivel, nodo) in enumerate(recorrido, start=1):
        print(f"{orden:>2}. {nodo.nombre} (nivel {nivel})")


def main():
    peliculas = catalogo.cargar(RUTA_DATOS)
    arbol = catalogo.crear_arbol_categorias(peliculas)

    print("Árbol de categorías")
    for linea in arbol.dibujar():
        print(linea)

    print(f"\nAltura: {arbol.altura()}")

    mostrar_recorrido("Preorden (cada categoría antes que sus subcategorías)", arbol.preorden())
    mostrar_recorrido("Postorden (cada categoría después de sus subcategorías)", arbol.postorden())
    mostrar_recorrido("Por niveles (de la raíz hacia abajo)", arbol.por_niveles())

    print("\nBúsquedas")
    print("Ruta a 'Cyberpunk':", " > ".join(arbol.ruta_a("Cyberpunk")))

    pelicula, ruta = arbol.ubicar_pelicula("Parasite")
    print(f"'{pelicula.titulo}' está en:", " > ".join(ruta))

    print("Categoría 'Western':", arbol.ruta_a("Western"))


if __name__ == "__main__":
    main()
