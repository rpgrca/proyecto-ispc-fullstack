from model.pujas import Puja
from .servicio import Servicio
from model.database import BaseDeDatos
from model.libro_diario import Venta


class ServicioLibroDiario(Servicio):
    PUJA_INVALIDA = "No se puede vender a una puja inválida"
    PUJA_INEXISTENTE = "No se puede vender a una puja inexistente"
    SIN_CLAVE = "No se puede ingresar sin clave"
    LOGIN_INVALIDO = "Usuario o contraseña inválida"
    PUJADOR_INVALIDO = "No se puede listar las compras de un pujador inválido"
    PUJADOR_INEXISTENTE = "No se puede listar las compras de un pujador inexistente"
    CERRAR_LOTE_INVALIDO = "No se puede cerrar un lote inválido"
    CERRAR_LOTE_INEXISTENTE = "No se puede cerrar un lote inexistente"

    COMISION_POR_VENTA = 0.1
    PRECIO_FINAL_MAS_IMPUESTOS = 1.12
    COMISION_A_CONSIGNATARIO = 0.97

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def convertir_en_venta(self, puja_uid: int) -> Venta:
        self._throw_if_not_positive(puja_uid, self.PUJA_INVALIDA)

        puja = self.__db.Pujas.buscar_por_uid(puja_uid)
        self._throw_if_invalid(puja, self.PUJA_INEXISTENTE)

        return self._vender_a(puja)

    def listar_compras_de(self, pujador_uid: int) -> list[Venta]:
        self._throw_if_not_positive(pujador_uid, self.PUJADOR_INVALIDO)

        pujador = self.__db.Usuarios.buscar_pujador_por_uid(pujador_uid)
        self._throw_if_invalid(pujador, self.PUJADOR_INEXISTENTE)

        return self.__db.Ventas.listar_compras_de(pujador)

    def registrar_venta_en(self, lote_uid: int) -> Venta:
        self._throw_if_not_positive(lote_uid, self.CERRAR_LOTE_INVALIDO)

        lote = self.__db.Lotes.buscar_por_uid(lote_uid)
        self._throw_if_invalid(lote, self.CERRAR_LOTE_INEXISTENTE)

        puja = self.__db.Pujas.buscar_ultima_puja(lote)
        if not puja:
            return None

        return self._vender_a(puja)

    def _vender_a(self, puja: Puja) -> Venta:
        comision = round(puja.obtener_monto() * self.COMISION_POR_VENTA, 2)
        precio_final = round((puja.obtener_monto() + comision) * self.PRECIO_FINAL_MAS_IMPUESTOS, 2)
        pago_consignatario = round(puja.obtener_monto() * self.COMISION_A_CONSIGNATARIO, 2)

        return self.__db.Ventas.crear(puja, precio_final, comision, pago_consignatario)
