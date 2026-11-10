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

    def test_bfs_recorre_por_niveles(self):
        recorrido = self.grafo.bfs("Matrix")
        self.assertEqual(
            [(p.titulo, distancia) for p, distancia in recorrido],
            [("Matrix", 0), ("Inception", 1), ("Terminator", 1), ("Interstellar", 2), ("Alien", 2)]
        )

    def test_dfs_recorre_en_profundidad(self):
        # Termina la rama de Inception (hasta Interstellar) antes de pasar a Terminator
        recorrido = self.grafo.dfs("Matrix")
        self.assertEqual(
            [(p.titulo, profundidad) for p, profundidad in recorrido],
            [("Matrix", 0), ("Inception", 1), ("Interstellar", 2), ("Terminator", 1), ("Alien", 2)]
        )

    def test_bfs_y_dfs_visitan_lo_mismo_en_otro_orden(self):
        en_anchura = titulos([p for p, _ in self.grafo.bfs("Matrix")])
        en_profundidad = titulos([p for p, _ in self.grafo.dfs("Matrix")])
        self.assertNotEqual(en_anchura, en_profundidad)
        self.assertEqual(sorted(en_anchura), sorted(en_profundidad))
        self.assertNotIn("Coco", en_anchura)

    def test_recorridos_de_pelicula_aislada_o_inexistente(self):
        self.assertEqual(titulos([p for p, _ in self.grafo.bfs("coco")]), ["Coco"])
        self.assertEqual(titulos([p for p, _ in self.grafo.dfs("coco")]), ["Coco"])
        self.assertIsNone(self.grafo.bfs("Titanic"))
        self.assertIsNone(self.grafo.dfs("Titanic"))


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

    def test_grados_de_separacion(self):
        niveles = catalogo.grados_de_separacion(self.grafo, "The Matrix")
        distancia, primer_nivel = niveles[0]
        self.assertEqual(distancia, 1)
        self.assertEqual(
            sorted(titulos(primer_nivel)),
            sorted(p.titulo for p, _ in self.grafo.vecinos("The Matrix"))
        )
        self.assertEqual([d for d, _ in niveles], list(range(1, len(niveles) + 1)))

    def test_grados_de_separacion_coinciden_con_el_camino_mas_corto(self):
        for distancia, peliculas_nivel in catalogo.grados_de_separacion(self.grafo, "The Matrix"):
            for pelicula in peliculas_nivel:
                camino = catalogo.camino_entre(self.grafo, "The Matrix", pelicula.titulo)
                self.assertEqual(len(camino) - 1, distancia)

    def test_explorar_en_profundidad(self):
        recorrido, no_alcanzadas = catalogo.explorar_en_profundidad(self.grafo, "The Matrix")
        self.assertEqual(recorrido[0], (self.grafo.buscar("The Matrix"), 0))
        # Arranca por la conexión más fuerte de Matrix
        self.assertEqual(recorrido[1][0].titulo, "Blade Runner 2049")
        self.assertIn("Coco", titulos(no_alcanzadas))
        self.assertEqual(len(recorrido) + len(no_alcanzadas), len(self.peliculas))

    def test_consultas_de_pelicula_inexistente(self):
        self.assertIsNone(catalogo.grados_de_separacion(self.grafo, "Titanic"))
        self.assertIsNone(catalogo.explorar_en_profundidad(self.grafo, "Titanic"))


if __name__ == "__main__":
    unittest.main()
