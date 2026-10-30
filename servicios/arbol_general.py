from collections import deque


class NodoCategoria:

    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
        self.peliculas = []

    def todas_las_peliculas(self):
        resultado = list(self.peliculas)

        for hijo in self.hijos:
            resultado.extend(hijo.todas_las_peliculas())

        return resultado


class ArbolCategorias:
    """Árbol general: cada categoría puede tener cualquier cantidad de subcategorías y de películas."""

    def __init__(self, nombre_raiz="Películas"):
        self.raiz = NodoCategoria(nombre_raiz)

    def agregar_categoria(self, padre, nombre):
        nodo = NodoCategoria(nombre)
        padre.hijos.append(nodo)
        return nodo

    def agregar_pelicula(self, pelicula, ruta):
        """Guarda la película en la categoría que indica la ruta (desde la raíz, sin incluirla), creando las que falten."""
        actual = self.raiz

        for nombre in ruta:
            siguiente = self._buscar_hijo(actual, nombre)

            if siguiente is None:
                siguiente = self.agregar_categoria(actual, nombre)

            actual = siguiente

        actual.peliculas.append(pelicula)

    def _buscar_hijo(self, nodo, nombre):
        for hijo in nodo.hijos:
            if hijo.nombre.lower() == nombre.lower():
                return hijo
        return None

    # Búsquedas

    def camino_a(self, nombre):
        """Lista de nodos desde la raíz hasta la categoría buscada, o None si no existe."""
        return self._camino_a(self.raiz, nombre.lower())

    def _camino_a(self, nodo, clave):
        if nodo.nombre.lower() == clave:
            return [nodo]

        for hijo in nodo.hijos:
            camino = self._camino_a(hijo, clave)

            if camino is not None:
                return [nodo] + camino

        return None

    def buscar_categoria(self, nombre):
        camino = self.camino_a(nombre)
        return camino[-1] if camino else None

    def ruta_a(self, nombre):
        camino = self.camino_a(nombre)
        return [nodo.nombre for nodo in camino] if camino else None

    def ubicar_pelicula(self, titulo):
        """Devuelve (pelicula, ruta de categorías) o None si el título no está en el árbol."""
        return self._ubicar_pelicula(self.raiz, titulo.lower(), [])

    def _ubicar_pelicula(self, nodo, clave, ruta):
        ruta = ruta + [nodo.nombre]

        for pelicula in nodo.peliculas:
            if pelicula.titulo.lower() == clave:
                return pelicula, ruta

        for hijo in nodo.hijos:
            resultado = self._ubicar_pelicula(hijo, clave, ruta)

            if resultado is not None:
                return resultado

        return None

    # Recorridos: devuelven una lista de (nivel, nodo)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, 0, resultado)
        return resultado

    def _preorden(self, nodo, nivel, resultado):
        resultado.append((nivel, nodo))

        for hijo in nodo.hijos:
            self._preorden(hijo, nivel + 1, resultado)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, 0, resultado)
        return resultado

    def _postorden(self, nodo, nivel, resultado):
        for hijo in nodo.hijos:
            self._postorden(hijo, nivel + 1, resultado)

        resultado.append((nivel, nodo))

    def por_niveles(self):
        resultado = []
        cola = deque([(0, self.raiz)])

        while cola:
            nivel, nodo = cola.popleft()
            resultado.append((nivel, nodo))

            for hijo in nodo.hijos:
                cola.append((nivel + 1, hijo))

        return resultado

    def altura(self):
        return max(nivel for nivel, _ in self.preorden()) + 1

    def dibujar(self):
        lineas = [self._etiqueta(self.raiz)]
        self._dibujar_hijos(self.raiz, "", lineas)
        return lineas

    def _dibujar_hijos(self, nodo, prefijo, lineas):
        for i, hijo in enumerate(nodo.hijos):
            es_ultimo = i == len(nodo.hijos) - 1
            rama = "└── " if es_ultimo else "├── "

            lineas.append(prefijo + rama + self._etiqueta(hijo))
            self._dibujar_hijos(hijo, prefijo + ("    " if es_ultimo else "│   "), lineas)

    def _etiqueta(self, nodo):
        return f"{nodo.nombre} ({len(nodo.todas_las_peliculas())})"
