from model.usuarios import Pujador
from model.lotes import Lote


class Puja:
    def __init__(self, monto: int, pujador: Pujador, lote: Lote):
        self.__monto = monto
        self.__pujador = pujador
        self.__lote = lote

    def obtener_monto(self) -> int:
        return self.__monto

    def obtener_pujador(self) -> Pujador:
        return self.__pujador

    def obtener_lote(self) -> Lote:
        return self.__lote



class Pujas:
    def agregar(self, monto: int, pujador: Pujador, lote: Lote) -> Puja:
        pass
    def buscar_por_monto(self, monto: int) -> Puja:
        pass
