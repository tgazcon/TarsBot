import unittest
from pathlib import Path

from servicios import catalogo
from servicios.heap import MonticuloMaximo

RUTA_DATOS = Path(__file__).parent.parent / "datos" / "peliculas.json"


def vaciar(monticulo):
    salida = []
    while not monticulo.esta_vacio():
        salida.append(monticulo.extraer_maximo())
    return salida


class TestMonticulo(unittest.TestCase):

    def test_extrae_de_mayor_a_menor(self):
        monticulo = MonticuloMaximo()
        for prioridad, nombre in [(5, "e"), (9, "i"), (1, "a"), (7, "g"), (3, "c")]:
            monticulo.insertar(prioridad, nombre)

        self.assertEqual(monticulo.ver_maximo(), (9, "i"))
        self.assertEqual(vaciar(monticulo), [(9, "i"), (7, "g"), (5, "e"), (3, "c"), (1, "a")])

    def test_en_un_empate_sale_primero_el_que_entro_antes(self):
        monticulo = MonticuloMaximo()
        for nombre in ["a", "b", "c", "d"]:
            monticulo.insertar(5, nombre)

        self.assertEqual([n for _, n in vaciar(monticulo)], ["a", "b", "c", "d"])

    def test_construir_desde_lista_da_el_mismo_orden(self):
        elementos = [4, 10, 3, 8, 1, 9, 2, 7]
        monticulo = MonticuloMaximo.construir(elementos, lambda x: x)
        self.assertEqual([e for _, e in vaciar(monticulo)], sorted(elementos, reverse=True))

    def test_monticulo_vacio(self):
        monticulo = MonticuloMaximo()
        self.assertTrue(monticulo.esta_vacio())
        self.assertIsNone(monticulo.ver_maximo())
        self.assertIsNone(monticulo.extraer_maximo())


class TestRanking(unittest.TestCase):

    def setUp(self):
        self.peliculas = catalogo.cargar(RUTA_DATOS)

    def test_top_valoradas_coincide_con_ordenar(self):
        esperado = sorted(self.peliculas, key=lambda p: p.valoracion, reverse=True)[:10]
        self.assertEqual(catalogo.top_valoradas(self.peliculas), esperado)

    def test_top_n_mayor_a_la_cantidad_devuelve_todas(self):
        self.assertEqual(len(catalogo.top_valoradas(self.peliculas, 100)), len(self.peliculas))

    def test_recomendar_ordena_por_puntaje_y_excluye_la_referencia(self):
        interstellar = catalogo.buscar_por_titulo(self.peliculas, "Interstellar")
        ranking = catalogo.recomendar(self.peliculas, interstellar)

        puntajes = [puntaje for puntaje, _ in ranking]
        self.assertEqual(puntajes, sorted(puntajes, reverse=True))
        self.assertNotIn(interstellar, [p for _, p in ranking])
        self.assertEqual(ranking[0][1].titulo, "Inception")


if __name__ == "__main__":
    unittest.main()
