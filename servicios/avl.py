class NodoAVL:

    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class ArbolAVL:
    """Árbol binario de búsqueda por título que se reequilibra solo al insertar."""

    def __init__(self):
        self.raiz = None
        self.rotaciones = 0

    def insertar(self, pelicula):
        self.raiz = self._insertar(self.raiz, pelicula)

    def _insertar(self, actual, pelicula):
        if actual is None:
            return NodoAVL(pelicula)

        if pelicula.titulo.lower() < actual.pelicula.titulo.lower():
            actual.izquierda = self._insertar(actual.izquierda, pelicula)
        else:
            actual.derecha = self._insertar(actual.derecha, pelicula)

        return self._reequilibrar(actual)

    def _reequilibrar(self, nodo):
        self._actualizar_altura(nodo)
        balance = self._balance(nodo)

        if balance > 1:
            # Izquierda-Derecha: primero se rota el hijo a la izquierda
            if self._balance(nodo.izquierda) < 0:
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)

        if balance < -1:
            # Derecha-Izquierda: primero se rota el hijo a la derecha
            if self._balance(nodo.derecha) > 0:
                nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    def _rotar_derecha(self, y):
        x = y.izquierda
        y.izquierda = x.derecha
        x.derecha = y

        self._actualizar_altura(y)
        self._actualizar_altura(x)
        self.rotaciones += 1
        return x

    def _rotar_izquierda(self, x):
        y = x.derecha
        x.derecha = y.izquierda
        y.izquierda = x

        self._actualizar_altura(x)
        self._actualizar_altura(y)
        self.rotaciones += 1
        return y

    @staticmethod
    def _altura_nodo(nodo):
        return nodo.altura if nodo is not None else 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(
            self._altura_nodo(nodo.izquierda),
            self._altura_nodo(nodo.derecha)
        )

    def _balance(self, nodo):
        return self._altura_nodo(nodo.izquierda) - self._altura_nodo(nodo.derecha)

    def altura(self):
        return self._altura_nodo(self.raiz)

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
