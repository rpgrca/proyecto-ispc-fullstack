from abc import ABC, abstractmethod
from model.articulos import Articulo
from model.serialization import Serializable
from model.subastas import Subasta


class Lote(Serializable):
    def __init__(self, uid: int, subasta: Subasta, articulo: Articulo, base: int, orden: int):
        self.__uid = uid
        self.__subasta = subasta
        self.__articulo = articulo
        self.__base = base
        self.__orden = orden

    def obtener_uid(self) -> int:
        return self.__uid

    def obtener_subasta_uid(self) -> int:
        return self.__subasta.obtener_uid()

    def obtener_precio_base(self) -> int:
        return self.__base

    def obtener_orden(self) -> int:
        return self.__orden

    def obtener_titulo_articulo(self) -> str:
        return self.__articulo.obtener_titulo()

    def obtener_articulo_uid(self) -> int:
        return self.__articulo.obtener_uid()

    def serialize(self):
        return {"articulo": self.__articulo.serialize(), "base": self.__base, "orden": self.__orden}


class Lotes(ABC):
    @abstractmethod
    def agregar(self, subasta: Subasta, articulo: Articulo, base: int, orden: int) -> None:
        pass

    @abstractmethod
    def contar_lotes(self, subasta: Subasta) -> int:
        pass

    @abstractmethod
    def obtener(self, subasta: Subasta, orden: int) -> Lote:
        pass

    @abstractmethod
    def buscar_por_uid(self, lote_uid: int) -> Lote:
        pass

    @abstractmethod
    def listar(self, subasta: Subasta) -> list[Lote]:
        pass

    @abstractmethod
    def existe_con_articulo(self, articulo: Articulo) -> bool:
        pass
