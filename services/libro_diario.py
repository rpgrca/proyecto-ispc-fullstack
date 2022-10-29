from .servicio import Servicio
from model.database import BaseDeDatos


class ServicioLibroDiario(Servicio):
    PUJA_INVALIDA = "No se puede vender a una puja inválida"
    PUJA_INEXISTENTE = "No se puede vender a una puja inexistente"
    SIN_CLAVE = "No se puede ingresar sin clave"
    LOGIN_INVALIDO = "Usuario o contraseña inválida"
    COMISION_POR_VENTA = 0.1
    PRECIO_FINAL_MAS_IMPUESTOS = 1.12
    COMISION_A_CONSIGNATARIO = 0.97

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, puja_uid: int):
        self._throw_if_not_positive(puja_uid, self.PUJA_INVALIDA)

        puja = self.__db.Pujas.buscar_por_uid(puja_uid)
        self._throw_if_invalid(puja, self.PUJA_INEXISTENTE)

        comision = puja.obtener_monto() * self.COMISION_POR_VENTA
        precio_final = (puja.obtener_monto() + comision) * self.PRECIO_FINAL_MAS_IMPUESTOS
        pago_consignatario = puja.obtener_monto() * self.COMISION_A_CONSIGNATARIO

        self.__db.Ventas.crear(puja, comision, precio_final, pago_consignatario)
