from model.articulos import Articulo
from model.subastas import Subasta


class Lote:
    def __init__(self, articulo: Articulo, base: float):
        self.__base = base

    def obtener_precio_base(self) -> float:
        return self.__base


class Lotes:
    def crear(self, subasta: Subasta, articulo: Articulo, base: float):
        pass


class LotesImplementadoConLista(Lotes):
    def __init__(self):
        self.__lotes_para_subastar = []

    def crear(self, subasta: Subasta, articulo: Articulo, base: float) -> Lote:
        lote = Lote(articulo, base)
        self.__lotes_para_subastar.append(lote)
        return lote
