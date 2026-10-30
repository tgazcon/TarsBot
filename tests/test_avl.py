import math
import random
import unittest
from pathlib import Path

from modelos.pelicula import Pelicula
from servicios import catalogo
from servicios.arbol import ArbolPeliculas
from servicios.avl import ArbolAVL

RUTA_DATOS = Path(__file__).parent.parent / "datos" / "peliculas.json"


def crear_pelicula(titulo):
    return Pelicula(titulo, "Director", 2000, "Drama", 7.0)


def armar(titulos):
    arbol = ArbolAVL()
    for titulo in titulos:
        arbol.insertar(crear_pelicula(titulo))
    return arbol


def titulos_preorder(arbol):
    return [p.titulo for p in arbol.preorder()]


def es_avl(nodo):
    """Devuelve la altura del subárbol, o lanza AssertionError si algún nodo está desbalanceado."""
    if nodo is None:
        return 0
    izquierda = es_avl(nodo.izquierda)
    derecha = es_avl(nodo.derecha)
    assert abs(izquierda - derecha) <= 1, nodo.pelicula.titulo
    assert nodo.altura == 1 + max(izquierda, derecha), nodo.pelicula.titulo
    return nodo.altura


class TestRotaciones(unittest.TestCase):

    def test_izquierda_izquierda_rota_a_la_derecha(self):
        arbol = armar(["C", "B", "A"])
        self.assertEqual(titulos_preorder(arbol), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 1)

    def test_derecha_derecha_rota_a_la_izquierda(self):
        arbol = armar(["A", "B", "C"])
        self.assertEqual(titulos_preorder(arbol), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 1)

    def test_izquierda_derecha_hace_rotacion_doble(self):
        arbol = armar(["C", "A", "B"])
        self.assertEqual(titulos_preorder(arbol), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 2)

    def test_derecha_izquierda_hace_rotacion_doble(self):
        arbol = armar(["A", "C", "B"])
        self.assertEqual(titulos_preorder(arbol), ["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 2)

    def test_insertar_en_orden_no_rota_si_ya_esta_balanceado(self):
        arbol = armar(["B", "A", "C"])
        self.assertEqual(arbol.rotaciones, 0)


class TestBalance(unittest.TestCase):

    def test_insercion_ordenada_mantiene_balance(self):
        titulos = [f"Pelicula {i:04d}" for i in range(1000)]
        arbol = armar(titulos)
        es_avl(arbol.raiz)
        self.assertLessEqual(arbol.altura(), 1.45 * math.log2(len(titulos) + 2))

    def test_insercion_descendente_mantiene_balance(self):
        titulos = [f"Pelicula {i:04d}" for i in range(1000)][::-1]
        es_avl(armar(titulos).raiz)

    def test_insercion_aleatoria_mantiene_balance(self):
        titulos = [f"Pelicula {i:04d}" for i in range(1000)]
        random.Random(1).shuffle(titulos)
        es_avl(armar(titulos).raiz)

    def test_inorder_queda_ordenado(self):
        titulos = [f"Pelicula {i:04d}" for i in range(200)]
        random.Random(2).shuffle(titulos)
        resultado = [p.titulo for p in armar(titulos).inorder()]
        self.assertEqual(resultado, sorted(titulos))

    def test_arbol_vacio(self):
        arbol = ArbolAVL()
        self.assertEqual(arbol.altura(), 0)
        self.assertIsNone(arbol.buscar("Matrix"))
        self.assertEqual(arbol.inorder(), [])


class TestConCatalogo(unittest.TestCase):

    def setUp(self):
        self.peliculas = catalogo.cargar(RUTA_DATOS)
        ordenadas = sorted(self.peliculas, key=lambda p: p.titulo.lower())
        self.avl = ArbolAVL()
        self.bst = ArbolPeliculas()
        for pelicula in ordenadas:
            self.avl.insertar(pelicula)
            self.bst.insertar(pelicula)

    def test_bst_con_titulos_ordenados_degenera_en_lista(self):
        self.assertEqual(self.bst.altura(), len(self.peliculas))

    def test_avl_con_los_mismos_titulos_queda_chico(self):
        es_avl(self.avl.raiz)
        self.assertLessEqual(self.avl.altura(), 1.45 * math.log2(len(self.peliculas) + 2))

    def test_ambos_encuentran_lo_mismo(self):
        for pelicula in self.peliculas:
            self.assertIs(self.avl.buscar(pelicula.titulo), pelicula)
            self.assertIs(self.bst.buscar(pelicula.titulo), pelicula)

    def test_buscar_inexistente(self):
        self.assertIsNone(self.avl.buscar("No existe"))

    def test_buscar_ignora_mayusculas(self):
        self.assertEqual(self.avl.buscar("iNtErStElLaR").titulo, "Interstellar")


if __name__ == "__main__":
    unittest.main()


# verifica las cuatro rotaciones sobre ejemplos de tres nodos (forma del árbol y cantidad de rotaciones),
#  que después de insertar 1.000 títulos en orden ascendente, descendente y aleatorio todos los nodos tienen balance entre -1 y 1
#  y su altura guardada es correcta, que la altura queda por debajo de 1,45 · log₂(n + 2), que el recorrido inorder sale ordenado,
#  y que con el catálogo real el BST llega a altura 30 y el AVL a 5 con los mismos resultados de búsqueda.