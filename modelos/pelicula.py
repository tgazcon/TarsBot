class Pelicula:
    def __init__(self, titulo: str, director: str, estreno: int, genero: str, valoracion: float = 0.0, subgenero: str = ""):
        self._titulo = titulo
        self._director = director
        self._estreno = estreno
        self._genero = genero
        self._valoracion = valoracion
        self._subgenero = subgenero

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def director(self) -> str:
        return self._director

    @property
    def estreno(self) -> int:
        return self._estreno

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def subgenero(self) -> str:
        return self._subgenero

    @property
    def valoracion(self) -> float:
        return self._valoracion

    def __repr__(self) -> str:
        return f"Pelicula({self._titulo}, {self._estreno}, {self._genero}, {self._valoracion})"
