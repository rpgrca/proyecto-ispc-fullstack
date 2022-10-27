from model.articulos import Articulo
from model.serialization import Serializable
from model.subastas import Subasta


class Lote(Serializable):
    def __init__(self, subasta: Subasta, articulo: Articulo, base: int, orden: int):
        self.__subasta = subasta
        self.__articulo = articulo
        self.__base = base
        self.__orden = orden

    def obtener_subasta_uid(self) -> int:
        return self.__subasta.obtener_uid()

    def obtener_precio_base(self) -> int:
        return self.__base

    def obtener_orden(self) -> int:
        return self.__orden

    def serialize(self):
        return {"articulo": self.__articulo.serialize(), "base": self.__base, "orden": self.__orden}


class Lotes:
    def agregar(self, subasta: Subasta, articulo: Articulo, base: int, orden: int) -> None:
        pass

    def contar_lotes(self, subasta: Subasta) -> int:
        pass

    def obtener(self, subasta: Subasta, orden: int) -> Lote:
        pass
