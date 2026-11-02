class MonticuloMaximo:
    """Heap binaria de máximos sobre una lista: el padre de i está en (i - 1) // 2 y sus hijos en 2i + 1 y 2i + 2."""

    def __init__(self):
        self._datos = []
        self._contador = 0

    @classmethod
    def construir(cls, elementos, prioridad):
        """Arma la heap desde una lista en O(n), bajando cada nodo interno de abajo hacia arriba."""
        monticulo = cls()

        for elemento in elementos:
            monticulo._datos.append((prioridad(elemento), monticulo._contador, elemento))
            monticulo._contador += 1

        for i in range(len(monticulo._datos) // 2 - 1, -1, -1):
            monticulo._bajar(i)

        return monticulo

    def __len__(self):
        return len(self._datos)

    def esta_vacio(self):
        return len(self._datos) == 0

    def insertar(self, prioridad, elemento):
        self._datos.append((prioridad, self._contador, elemento))
        self._contador += 1
        self._subir(len(self._datos) - 1)

    def ver_maximo(self):
        """Devuelve (prioridad, elemento) del mayor sin sacarlo, o None si está vacía."""
        if self.esta_vacio():
            return None

        prioridad, _, elemento = self._datos[0]
        return prioridad, elemento

    def extraer_maximo(self):
        """Saca y devuelve (prioridad, elemento) del mayor, o None si está vacía."""
        if self.esta_vacio():
            return None

        prioridad, _, elemento = self._datos[0]
        ultimo = self._datos.pop()

        if self._datos:
            self._datos[0] = ultimo
            self._bajar(0)

        return prioridad, elemento

    # En un empate sale primero el que entró antes
    def _tiene_mas_prioridad(self, i, j):
        a, b = self._datos[i], self._datos[j]

        if a[0] != b[0]:
            return a[0] > b[0]

        return a[1] < b[1]

    def _intercambiar(self, i, j):
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]

    def _subir(self, i):
        while i > 0:
            padre = (i - 1) // 2

            if not self._tiene_mas_prioridad(i, padre):
                break

            self._intercambiar(i, padre)
            i = padre

    def _bajar(self, i):
        cantidad = len(self._datos)

        while True:
            mayor = i
            izquierdo = 2 * i + 1
            derecho = 2 * i + 2

            if izquierdo < cantidad and self._tiene_mas_prioridad(izquierdo, mayor):
                mayor = izquierdo

            if derecho < cantidad and self._tiene_mas_prioridad(derecho, mayor):
                mayor = derecho

            if mayor == i:
                break

            self._intercambiar(i, mayor)
            i = mayor
