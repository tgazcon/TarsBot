class Nodo:

    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.izquierda = None
        self.derecha = None


class ArbolPeliculas:

    def __init__(self):
        self.raiz = None

    # Insertar y buscar son iterativos: con datos ordenados el árbol degenera
    # en una lista y la recursión superaría el límite de Python.
    def insertar(self, pelicula):
        nuevo = Nodo(pelicula)

        if self.raiz is None:
            self.raiz = nuevo
            return

        clave = pelicula.titulo.lower()
        actual = self.raiz

        while True:
            if clave < actual.pelicula.titulo.lower():
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    return
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    return
                actual = actual.derecha

    def buscar(self, titulo):
        clave = titulo.lower()
        actual = self.raiz

        while actual is not None:
            clave_actual = actual.pelicula.titulo.lower()

            if clave == clave_actual:
                return actual.pelicula

            if clave < clave_actual:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return None

    def altura(self):
        if self.raiz is None:
            return 0

        altura = 0
        nivel = [self.raiz]

        while nivel:
            altura += 1
            siguiente = []
            for nodo in nivel:
                if nodo.izquierda is not None:
                    siguiente.append(nodo.izquierda)
                if nodo.derecha is not None:
                    siguiente.append(nodo.derecha)
            nivel = siguiente

        return altura

    def inorder(self):
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, actual, resultado):

        if actual is not None:
            self._inorder(actual.izquierda, resultado)
            resultado.append(actual.pelicula)
            self._inorder(actual.derecha, resultado)

    def preorder(self):
        resultado = []
        self._preorder(self.raiz, resultado)
        return resultado

    def _preorder(self, actual, resultado):

        if actual is not None:
            resultado.append(actual.pelicula)
            self._preorder(actual.izquierda, resultado)
            self._preorder(actual.derecha, resultado)

    def postorder(self):
        resultado = []
        self._postorder(self.raiz, resultado)
        return resultado

    def _postorder(self, actual, resultado):

        if actual is not None:
            self._postorder(actual.izquierda, resultado)
            self._postorder(actual.derecha, resultado)
            resultado.append(actual.pelicula)


def crear_arbol_equilibrado(peliculas):

    peliculas_ordenadas = sorted(
        peliculas,
        key=lambda pelicula: pelicula.titulo.lower()
    )

    arbol = ArbolPeliculas()

    _agregar_mitad(
        arbol,
        peliculas_ordenadas,
        0,
        len(peliculas_ordenadas) - 1
    )

    return arbol


def _agregar_mitad(arbol, peliculas, inicio, fin):

    if inicio <= fin:

        medio = (inicio + fin) // 2

        arbol.insertar(peliculas[medio])

        _agregar_mitad(
            arbol,
            peliculas,
            inicio,
            medio - 1
        )

        _agregar_mitad(
            arbol,
            peliculas,
            medio + 1,
            fin
        )