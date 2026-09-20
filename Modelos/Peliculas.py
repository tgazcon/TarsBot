class Pelicula:
    def __init__(self, titulo: str, director: str, estreno: int, genero: str, valoracion: float = 0.0):
        self._titulo = titulo
        self._director = director
        self._estreno = estreno
        self._genero = genero
        self._valoracion = valoracion

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def director(self) -> str:
        return self._director

    @property
    def anio(self) -> int:
        return self._estreno

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def valoracion(self) -> float:
        return self._valoracion

    def es_del_genero(self, genero: str) -> bool:
        return self._genero.lower() == genero.lower()

    def comparten_genero(self, otra: "Pelicula") -> bool:
        return self.es_del_genero(otra.genero)

    def __repr__(self) -> str:
        return f"Pelicula({self._titulo}, {self._estreno}, {self._genero}, {self._valoracion})"
