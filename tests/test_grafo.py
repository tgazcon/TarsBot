import unittest
from pathlib import Path

from modelos.pelicula import Pelicula
from servicios import catalogo
from servicios.grafo import GrafoPeliculas

RUTA_DATOS = Path(__file__).parent.parent / "datos" / "peliculas.json"


def crear_pelicula(titulo):
    return Pelicula(titulo, "Director", 2000, "Ciencia ficción", 7.0)


def titulos(peliculas):
    return [p.titulo for p in peliculas]


class TestGrafoChico(unittest.TestCase):

    def setUp(self):
        # Matrix une a Inception y Terminator; Inception lleva a Interstellar y Terminator a Alien; Coco queda aislada
        p = {nombre: crear_pelicula(nombre) for nombre in
             ["Matrix", "Inception", "Terminator", "Interstellar", "Alien", "Coco"]}
        self.grafo = GrafoPeliculas()
        for pelicula in p.values():
            self.grafo.agregar_vertice(pelicula)
        for a, b in [("Matrix", "Inception"), ("Matrix", "Terminator"),
                     ("Inception", "Interstellar"), ("Terminator", "Alien")]:
            self.grafo.agregar_arista(p[a], p[b], 1.0)

    def test_es_no_dirigido(self):
        self.assertEqual(titulos([p for p, _ in self.grafo.vecinos("Matrix")]), ["Inception", "Terminator"])
        self.assertEqual(titulos([p for p, _ in self.grafo.vecinos("Inception")]), ["Interstellar", "Matrix"])

    def test_camino_mas_corto(self):
        camino = self.grafo.camino_mas_corto("interstellar", "Alien")
        self.assertEqual(titulos(camino), ["Interstellar", "Inception", "Matrix", "Terminator", "Alien"])

    def test_sin_camino_o_pelicula_inexistente(self):
        self.assertIsNone(self.grafo.camino_mas_corto("Matrix", "Coco"))
        self.assertIsNone(self.grafo.camino_mas_corto("Matrix", "Titanic"))
        self.assertIsNone(self.grafo.vecinos("Titanic"))


class TestGrafoCatalogo(unittest.TestCase):

    def setUp(self):
        self.peliculas = catalogo.cargar(RUTA_DATOS)
        self.grafo = catalogo.crear_grafo(self.peliculas)

    def test_un_vertice_por_pelicula(self):
        self.assertEqual(self.grafo.cantidad_vertices(), len(self.peliculas))

    def test_el_peso_es_la_afinidad(self):
        # Mismo género (1,0) y mismo director (1,0)
        vecinos = dict((p.titulo, peso) for p, peso in self.grafo.vecinos("Inception"))
        self.assertEqual(vecinos["Interstellar"], 2.0)
        self.assertNotIn("Coco", vecinos)

    def test_camino_entre_generos(self):
        camino = catalogo.camino_entre(self.grafo, "The Matrix", "Gladiator")
        self.assertEqual(camino[0].titulo, "The Matrix")
        self.assertEqual(camino[-1].titulo, "Gladiator")
        self.assertIsNone(catalogo.camino_entre(self.grafo, "Coco", "The Matrix"))


if __name__ == "__main__":
    unittest.main()
