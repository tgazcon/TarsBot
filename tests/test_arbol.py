import unittest
from pathlib import Path

from modelos.pelicula import Pelicula
from servicios import catalogo
from servicios.arbol import ArbolPeliculas, crear_arbol_equilibrado

RUTA_DATOS = Path(__file__).parent.parent / "datos" / "peliculas.json"


def titulos(peliculas):
    return [p.titulo for p in peliculas]


def crear_pelicula(titulo):
    return Pelicula(titulo, "Director", 2000, "Drama", 7.0)


class TestArbolChico(unittest.TestCase):

    def setUp(self):
        # Mismo ejemplo que la consigna: Matrix en la raíz, Inception a la izquierda y Titanic a la derecha
        peliculas = [crear_pelicula("Titanic"), crear_pelicula("Matrix"), crear_pelicula("Inception")]
        self.arbol = crear_arbol_equilibrado(peliculas)

    def test_raiz_es_el_titulo_del_medio(self):
        self.assertEqual(self.arbol.raiz.pelicula.titulo, "Matrix")
        self.assertEqual(self.arbol.raiz.izquierda.pelicula.titulo, "Inception")
        self.assertEqual(self.arbol.raiz.derecha.pelicula.titulo, "Titanic")

    def test_inorder(self):
        self.assertEqual(titulos(self.arbol.inorder()), ["Inception", "Matrix", "Titanic"])

    def test_preorder(self):
        self.assertEqual(titulos(self.arbol.preorder()), ["Matrix", "Inception", "Titanic"])

    def test_postorder(self):
        self.assertEqual(titulos(self.arbol.postorder()), ["Inception", "Titanic", "Matrix"])


class TestArbolVacio(unittest.TestCase):

    def test_buscar_en_arbol_vacio(self):
        self.assertIsNone(ArbolPeliculas().buscar("Matrix"))

    def test_recorridos_de_arbol_vacio(self):
        arbol = ArbolPeliculas()
        self.assertEqual(arbol.inorder(), [])
        self.assertEqual(arbol.preorder(), [])
        self.assertEqual(arbol.postorder(), [])


class TestArbolCatalogo(unittest.TestCase):

    def setUp(self):
        self.peliculas = catalogo.cargar(RUTA_DATOS)
        self.arbol = catalogo.crear_arbol(self.peliculas)

    def test_buscar_pelicula_existente(self):
        pelicula = catalogo.buscar_por_titulo_arbol(self.arbol, "Interstellar")
        self.assertIsNotNone(pelicula)
        self.assertEqual(pelicula.director, "Christopher Nolan")

    def test_buscar_ignora_mayusculas(self):
        pelicula = catalogo.buscar_por_titulo_arbol(self.arbol, "iNtErStElLaR")
        self.assertEqual(pelicula.titulo, "Interstellar")

    def test_buscar_pelicula_inexistente(self):
        self.assertIsNone(catalogo.buscar_por_titulo_arbol(self.arbol, "No existe"))

    def test_arbol_y_secuencial_encuentran_lo_mismo(self):
        for pelicula in self.peliculas:
            self.assertIs(
                catalogo.buscar_por_titulo_arbol(self.arbol, pelicula.titulo),
                catalogo.buscar_por_titulo(self.peliculas, pelicula.titulo)
            )

    def test_listar_alfabetico_esta_ordenado_y_completo(self):
        resultado = catalogo.listar_alfabetico(self.arbol)
        self.assertEqual(len(resultado), len(self.peliculas))
        self.assertEqual(
            titulos(resultado),
            sorted(titulos(self.peliculas), key=str.lower)
        )


if __name__ == "__main__":
    unittest.main()
