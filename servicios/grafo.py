from collections import deque


class GrafoPeliculas:
    """Grafo no dirigido y pesado con lista de adyacencia.

    Cada vértice es una película (identificada por su título, sin distinguir mayúsculas)
    y cada arista une dos películas parecidas, con la afinidad como peso.
    """

    def __init__(self):
        self._peliculas = {}
        self._adyacentes = {}
        self._cantidad_aristas = 0

    @staticmethod
    def _clave(titulo):
        return titulo.lower()

    def agregar_vertice(self, pelicula):
        clave = self._clave(pelicula.titulo)

        if clave not in self._peliculas:
            self._peliculas[clave] = pelicula
            self._adyacentes[clave] = {}

    def agregar_arista(self, a, b, peso):
        clave_a = self._clave(a.titulo)
        clave_b = self._clave(b.titulo)

        if clave_b not in self._adyacentes[clave_a]:
            self._cantidad_aristas += 1

        self._adyacentes[clave_a][clave_b] = peso
        self._adyacentes[clave_b][clave_a] = peso

    def buscar(self, titulo):
        return self._peliculas.get(self._clave(titulo))

    def cantidad_vertices(self):
        return len(self._peliculas)

    def cantidad_aristas(self):
        return self._cantidad_aristas

    def vecinos(self, titulo):
        """Lista de (película, peso) de mayor a menor peso, o None si la película no está."""
        clave = self._clave(titulo)

        if clave not in self._adyacentes:
            return None

        return sorted(
            ((self._peliculas[vecino], peso) for vecino, peso in self._adyacentes[clave].items()),
            key=lambda par: (-par[1], par[0].titulo.lower())
        )

    def camino_mas_corto(self, origen, destino):
        """Películas del camino con menos saltos (búsqueda en anchura), o None si no hay camino o alguna no está."""
        clave_origen = self._clave(origen)
        clave_destino = self._clave(destino)

        if clave_origen not in self._adyacentes or clave_destino not in self._adyacentes:
            return None

        padre = {clave_origen: None}
        cola = deque([clave_origen])

        while cola and clave_destino not in padre:
            actual = cola.popleft()

            for vecino in self._adyacentes[actual]:
                if vecino not in padre:
                    padre[vecino] = actual
                    cola.append(vecino)

        if clave_destino not in padre:
            return None

        camino = []
        actual = clave_destino

        while actual is not None:
            camino.append(self._peliculas[actual])
            actual = padre[actual]

        return camino[::-1]
