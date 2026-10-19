class Nodo:

    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.izquierda = None
        self.derecha = None


class ArbolPeliculas:

    def __init__(self):
        self.raiz = None

    def insertar(self, pelicula):
        nuevo = Nodo(pelicula)

        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar(self.raiz, nuevo)

    def _insertar(self, actual, nuevo):

        if nuevo.pelicula.titulo.lower() < actual.pelicula.titulo.lower():

            if actual.izquierda is None:
                actual.izquierda = nuevo
            else:
                self._insertar(actual.izquierda, nuevo)

        else:

            if actual.derecha is None:
                actual.derecha = nuevo
            else:
                self._insertar(actual.derecha, nuevo)

    def buscar(self, titulo):
        return self._buscar(self.raiz, titulo)

    def _buscar(self, actual, titulo):

        if actual is None:
            return None

        if actual.pelicula.titulo.lower() == titulo.lower():
            return actual.pelicula

        if titulo.lower() < actual.pelicula.titulo.lower():
            return self._buscar(actual.izquierda, titulo)

        else:
            return self._buscar(actual.derecha, titulo)

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