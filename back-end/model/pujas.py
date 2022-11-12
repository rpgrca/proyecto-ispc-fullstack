from abc import ABC, abstractmethod
from model.usuarios import Pujador
from model.serialization import Serializable
from model.lotes import Lote


class Puja(Serializable):
    def __init__(self, uid: int, pujador: Pujador, lote: Lote, monto: int):
        self.__uid = uid
        self.__monto = monto
        self.__pujador = pujador
        self.__lote = lote

    def obtener_uid(self) -> int:
        return self.__uid

    def obtener_monto(self) -> int:
        return self.__monto

    def obtener_pujador(self) -> Pujador:
        return self.__pujador

    def obtener_lote(self) -> Lote:
        return self.__lote

    def serialize(self):
        return {"monto": self.__monto, "lote": self.__lote.obtener_uid(), "pujador": self.__lote.obtener_uid()}


class Pujas(ABC):
    @abstractmethod
    def agregar(self, pujador: Pujador, lote: Lote, monto: int):
        pass

    @abstractmethod
    def buscar_ultima_puja(self, lote: Lote) -> Puja:
        pass

    @abstractmethod
    def buscar_por_uid(self, uid: int) -> Puja:
        pass

    @abstractmethod
    def buscar_por_lote(self, lote: Lote) -> list[Puja]:
        pass
