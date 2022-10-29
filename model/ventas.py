# venta.py
#
# crear(puja)
# listar_compras_para(pujador)
from model.pujas import Puja


class Venta:
    def __init__(self, puja: Puja, precio_final: float, comision: float, pago_a_consignatario: float):
        self.__puja = puja
        self.__precio = precio_final
        self.__comision = comision
        self.__pago_a_consignatario = pago_a_consignatario

    def obtener_nombre_lote(self) -> str:
        return self.__puja.obtener_titulo_lote()

    def obtener_nombre_ganador(self) -> str:
        return self.__puja.obtener_pujador().obtener_nombre()

    def obtener_precio_final(self) -> float:
        return self.__precio

    def obtener_comision(self) -> float:
        return self.__comision

    def obtener_pago_a_consignatario(self) -> float:
        return self.__pago_a_consignatario
 