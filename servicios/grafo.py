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

    def peliculas(self):
        return list(self._peliculas.values())

    def _vecinos_ordenados(self, clave):
        """Claves de los vecinos, de la conexión más fuerte a la más débil (y por título si empatan)."""
        return sorted(
            self._adyacentes[clave],
            key=lambda vecino: (-self._adyacentes[clave][vecino], vecino)
        )

    def vecinos(self, titulo):
        """Lista de (película, peso) de mayor a menor peso, o None si la película no está."""
        clave = self._clave(titulo)

        if clave not in self._adyacentes:
            return None

        return [(self._peliculas[vecino], self._adyacentes[clave][vecino]) for vecino in self._vecinos_ordenados(clave)]

    def _bfs(self, clave_origen):
        """Búsqueda en anchura: devuelve el orden de visita, la distancia en saltos y el padre de cada vértice."""
        orden = [clave_origen]
        distancia = {clave_origen: 0}
        padre = {clave_origen: None}
        cola = deque([clave_origen])

        while cola:
            actual = cola.popleft()

            for vecino in self._vecinos_ordenados(actual):
                if vecino not in distancia:
                    distancia[vecino] = distancia[actual] + 1
                    padre[vecino] = actual
                    orden.append(vecino)
                    cola.append(vecino)

        return orden, distancia, padre

    def bfs(self, origen):
        """Lista de (película, distancia) en el orden en que la búsqueda en anchura las visita, o None si no está."""
        clave_origen = self._clave(origen)

        if clave_origen not in self._adyacentes:
            return None

        orden, distancia, _ = self._bfs(clave_origen)
        return [(self._peliculas[clave], distancia[clave]) for clave in orden]

    def dfs(self, origen):
        """Lista de (película, profundidad) en el orden en que la búsqueda en profundidad las visita, o None si no está."""
        clave_origen = self._clave(origen)

        if clave_origen not in self._adyacentes:
            return None

        visitados = set()
        recorrido = []
        self._dfs(clave_origen, 0, visitados, recorrido)
        return recorrido

    def _dfs(self, actual, profundidad, visitados, recorrido):
        visitados.add(actual)
        recorrido.append((self._peliculas[actual], profundidad))

        for vecino in self._vecinos_ordenados(actual):
            if vecino not in visitados:
                self._dfs(vecino, profundidad + 1, visitados, recorrido)

    def camino_mas_corto(self, origen, destino):
        """Películas del camino con menos saltos (búsqueda en anchura), o None si no hay camino o alguna no está."""
        clave_origen = self._clave(origen)
        clave_destino = self._clave(destino)

        if clave_origen not in self._adyacentes or clave_destino not in self._adyacentes:
            return None

        _, _, padre = self._bfs(clave_origen)

        if clave_destino not in padre:
            return None

        camino = []
        actual = clave_destino

        while actual is not None:
            camino.append(self._peliculas[actual])
            actual = padre[actual]

        return camino[::-1]
