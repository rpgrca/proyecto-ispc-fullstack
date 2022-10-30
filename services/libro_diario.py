from .servicio import Servicio
from model.database import BaseDeDatos
from model.ventas import Venta


class ServicioLibroDiario(Servicio):
    PUJA_INVALIDA = "No se puede vender a una puja inválida"
    PUJA_INEXISTENTE = "No se puede vender a una puja inexistente"
    SIN_CLAVE = "No se puede ingresar sin clave"
    LOGIN_INVALIDO = "Usuario o contraseña inválida"
    PUJADOR_INVALIDO = "No se puede listar las compras de un pujador inválido"
    PUJADOR_INEXISTENTE = "No se puede listar las compras de un pujador inexistente"

    COMISION_POR_VENTA = 0.1
    PRECIO_FINAL_MAS_IMPUESTOS = 1.12
    COMISION_A_CONSIGNATARIO = 0.97

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, puja_uid: int):
        self._throw_if_not_positive(puja_uid, self.PUJA_INVALIDA)

        puja = self.__db.Pujas.buscar_por_uid(puja_uid)
        self._throw_if_invalid(puja, self.PUJA_INEXISTENTE)

        comision = round(puja.obtener_monto() * self.COMISION_POR_VENTA, 2)
        precio_final = round((puja.obtener_monto() + comision) * self.PRECIO_FINAL_MAS_IMPUESTOS, 2)
        pago_consignatario = round(puja.obtener_monto() * self.COMISION_A_CONSIGNATARIO, 2)

        self.__db.Ventas.crear(puja, comision, precio_final, pago_consignatario)

    def listar_compras_de(self, pujador_uid: int) -> list[Venta]:
        self._throw_if_not_positive(pujador_uid, self.PUJADOR_INVALIDO)

        pujador = self.__db.Usuarios.buscar_pujador_por_uid(pujador_uid)
        self._throw_if_invalid(pujador, self.PUJADOR_INEXISTENTE)

        return self.__db.Ventas.listar_compras_de(pujador)
