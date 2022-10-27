from model.usuarios import Pujador
from model.lotes import Lote


class Puja:
    def __init__(self, uid: int, monto: int, pujador: Pujador, lote: Lote):
        self.__uid = uid
        self.__monto = monto
        self.__pujador = pujador
        self.__lote = lote

    def obtener_uid(self) -> int:
        return self.__uid

    def obtener_monto(self) -> int:
        return self.__monto

    def obtener_pujador_uid(self) -> int:
        return self.__pujador.obtener_uid()

    def obtener_lote_uid(self) -> int:
        return self.__lote.obtener_uid()


class Pujas:
    def agregar(self, monto: int, pujador: Pujador, lote: Lote):
        raise NotImplementedError()

    def buscar_por_monto(self, monto: int) -> Puja:
        raise NotImplementedError()

    def buscar_ultima_puja(self, lote: Lote) -> Puja:
        raise NotImplementedError()

    def buscar_por_uid(self, uid: int) -> Puja:
        raise NotImplementedError()
