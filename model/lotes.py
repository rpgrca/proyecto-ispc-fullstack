from model.articulos import Articulo


class Lote:
    def __init__(self, articulo: Articulo, base: float):
        self.__articulo = articulo
        self.__base = base

    def obtener_precio_base(self) -> float:
        return self.__base


class Lotes:
    def crear(self, articulo: Articulo, base: float):
        pass