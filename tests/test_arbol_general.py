import unittest
from pathlib import Path

from modelos.pelicula import Pelicula
from servicios import catalogo
from servicios.arbol_general import ArbolCategorias

RUTA_DATOS = Path(__file__).parent.parent / "datos" / "peliculas.json"


def crear_pelicula(titulo, genero="Drama", subgenero=""):
    return Pelicula(titulo, "Director", 2000, genero, 7.0, subgenero)


def nombres(recorrido):
    return [nodo.nombre for _, nodo in recorrido]


def titulos(peliculas):
    return [p.titulo for p in peliculas]


def crear_arbol_de_la_consigna():
    # Películas -> Ciencia ficción (Cyberpunk, Viajes temporales, Inteligencia artificial), Acción, Comedia
    arbol = ArbolCategorias("Películas")
    ciencia_ficcion = arbol.agregar_categoria(arbol.raiz, "Ciencia ficción")
    arbol.agregar_categoria(ciencia_ficcion, "Cyberpunk")
    arbol.agregar_categoria(ciencia_ficcion, "Viajes temporales")
    arbol.agregar_categoria(ciencia_ficcion, "Inteligencia artificial")
    arbol.agregar_categoria(arbol.raiz, "Acción")
    arbol.agregar_categoria(arbol.raiz, "Comedia")
    return arbol


class TestRecorridos(unittest.TestCase):

    def setUp(self):
        self.arbol = crear_arbol_de_la_consigna()

    def test_preorden(self):
        self.assertEqual(
            nombres(self.arbol.preorden()),
            ["Películas", "Ciencia ficción", "Cyberpunk", "Viajes temporales",
             "Inteligencia artificial", "Acción", "Comedia"]
        )

    def test_postorden(self):
        self.assertEqual(
            nombres(self.arbol.postorden()),
            ["Cyberpunk", "Viajes temporales", "Inteligencia artificial",
             "Ciencia ficción", "Acción", "Comedia", "Películas"]
        )

    def test_por_niveles(self):
        self.assertEqual(
            nombres(self.arbol.por_niveles()),
            ["Películas", "Ciencia ficción", "Acción", "Comedia",
             "Cyberpunk", "Viajes temporales", "Inteligencia artificial"]
        )

    def test_los_niveles_son_correctos(self):
        niveles = [(nivel, nodo.nombre) for nivel, nodo in self.arbol.preorden()]
        self.assertEqual(niveles[0], (0, "Películas"))
        self.assertEqual(niveles[1], (1, "Ciencia ficción"))
        self.assertEqual(niveles[2], (2, "Cyberpunk"))
        self.assertEqual(niveles[5], (1, "Acción"))

    def test_altura(self):
        self.assertEqual(self.arbol.altura(), 3)

    def test_arbol_con_solo_la_raiz(self):
        arbol = ArbolCategorias("Películas")
        self.assertEqual(nombres(arbol.preorden()), ["Películas"])
        self.assertEqual(arbol.altura(), 1)


class TestBusquedas(unittest.TestCase):

    def setUp(self):
        self.arbol = crear_arbol_de_la_consigna()

    def test_buscar_categoria_existente(self):
        self.assertEqual(self.arbol.buscar_categoria("Cyberpunk").nombre, "Cyberpunk")

    def test_buscar_categoria_ignora_mayusculas(self):
        self.assertEqual(self.arbol.buscar_categoria("ciencia FICCIÓN").nombre, "Ciencia ficción")

    def test_buscar_categoria_inexistente(self):
        self.assertIsNone(self.arbol.buscar_categoria("Western"))
        self.assertIsNone(self.arbol.ruta_a("Western"))

    def test_ruta_a_subcategoria(self):
        self.assertEqual(
            self.arbol.ruta_a("Viajes temporales"),
            ["Películas", "Ciencia ficción", "Viajes temporales"]
        )

    def test_ruta_a_la_raiz(self):
        self.assertEqual(self.arbol.ruta_a("Películas"), ["Películas"])

    def test_ubicar_pelicula(self):
        matrix = crear_pelicula("The Matrix")
        self.arbol.agregar_pelicula(matrix, ["Ciencia ficción", "Cyberpunk"])

        pelicula, ruta = self.arbol.ubicar_pelicula("the matrix")

        self.assertIs(pelicula, matrix)
        self.assertEqual(ruta, ["Películas", "Ciencia ficción", "Cyberpunk"])

    def test_ubicar_pelicula_inexistente(self):
        self.assertIsNone(self.arbol.ubicar_pelicula("Titanic"))


class TestAgregar(unittest.TestCase):

    def test_agregar_pelicula_crea_las_categorias_que_faltan(self):
        arbol = ArbolCategorias("Películas")
        arbol.agregar_pelicula(crear_pelicula("A"), ["Drama", "Crimen"])
        self.assertEqual(arbol.ruta_a("Crimen"), ["Películas", "Drama", "Crimen"])

    def test_agregar_pelicula_reutiliza_categorias_existentes(self):
        arbol = ArbolCategorias("Películas")
        arbol.agregar_pelicula(crear_pelicula("A"), ["Drama", "Crimen"])
        arbol.agregar_pelicula(crear_pelicula("B"), ["drama", "crimen"])
        arbol.agregar_pelicula(crear_pelicula("C"), ["Drama"])

        self.assertEqual(nombres(arbol.preorden()), ["Películas", "Drama", "Crimen"])
        self.assertEqual(titulos(arbol.buscar_categoria("Crimen").peliculas), ["A", "B"])
        self.assertEqual(titulos(arbol.buscar_categoria("Drama").peliculas), ["C"])

    def test_todas_las_peliculas_incluye_subcategorias(self):
        arbol = ArbolCategorias("Películas")
        arbol.agregar_pelicula(crear_pelicula("A"), ["Drama"])
        arbol.agregar_pelicula(crear_pelicula("B"), ["Drama", "Crimen"])
        arbol.agregar_pelicula(crear_pelicula("C"), ["Drama", "Social"])

        self.assertEqual(titulos(arbol.buscar_categoria("Drama").todas_las_peliculas()), ["A", "B", "C"])
        self.assertEqual(titulos(arbol.buscar_categoria("Crimen").todas_las_peliculas()), ["B"])


class TestDibujo(unittest.TestCase):

    def test_dibujar_muestra_la_jerarquia_con_cantidades(self):
        arbol = crear_arbol_de_la_consigna()
        arbol.agregar_pelicula(crear_pelicula("The Matrix"), ["Ciencia ficción", "Cyberpunk"])
        arbol.agregar_pelicula(crear_pelicula("Gladiator"), ["Acción"])

        self.assertEqual(
            arbol.dibujar(),
            [
                "Películas (2)",
                "├── Ciencia ficción (1)",
                "│   ├── Cyberpunk (1)",
                "│   ├── Viajes temporales (0)",
                "│   └── Inteligencia artificial (0)",
                "├── Acción (1)",
                "└── Comedia (0)",
            ]
        )


class TestCatalogoReal(unittest.TestCase):

    def setUp(self):
        self.peliculas = catalogo.cargar(RUTA_DATOS)
        self.arbol = catalogo.crear_arbol_categorias(self.peliculas)

    def test_la_raiz_contiene_todas_las_peliculas(self):
        self.assertEqual(len(self.arbol.raiz.todas_las_peliculas()), len(self.peliculas))

    def test_los_generos_son_los_hijos_de_la_raiz(self):
        generos = sorted({p.genero for p in self.peliculas}, key=str.lower)
        self.assertEqual([hijo.nombre for hijo in self.arbol.raiz.hijos], generos)

    def test_cada_pelicula_esta_en_su_genero_y_subgenero(self):
        for pelicula in self.peliculas:
            encontrada, ruta = catalogo.ubicar_pelicula(self.arbol, pelicula.titulo)
            self.assertIs(encontrada, pelicula)
            esperada = ["Películas", pelicula.genero] + ([pelicula.subgenero] if pelicula.subgenero else [])
            self.assertEqual(ruta, esperada)

    def test_peliculas_de_una_subcategoria(self):
        ruta, peliculas = catalogo.peliculas_de_categoria(self.arbol, "cyberpunk")
        self.assertEqual(ruta, ["Películas", "Ciencia ficción", "Cyberpunk"])
        self.assertEqual(titulos(peliculas), ["Blade Runner 2049", "The Matrix"])

    def test_peliculas_de_un_genero_incluyen_sus_subgeneros(self):
        _, peliculas = catalogo.peliculas_de_categoria(self.arbol, "Drama")
        esperadas = [p for p in self.peliculas if p.genero == "Drama"]
        self.assertCountEqual(titulos(peliculas), titulos(esperadas))

    def test_categoria_inexistente(self):
        self.assertIsNone(catalogo.peliculas_de_categoria(self.arbol, "Western"))

    def test_generos_sin_subcategorias_guardan_las_peliculas_directo(self):
        accion = self.arbol.buscar_categoria("Acción")
        self.assertEqual(accion.hijos, [])
        self.assertEqual(len(accion.peliculas), 4)

    def test_altura_del_catalogo(self):
        self.assertEqual(self.arbol.altura(), 3)


if __name__ == "__main__":
    unittest.main()
