from controller.controlador import Controlador
from model.database import BaseDeDatos
from services.libro_diario import ServicioLibroDiario


class ControladorLibroDiario(Controlador):
    LOTE_DESIERTO = "El lote ha quedado desierto"
    VENTA_EXITOSA = "El lote ha sido vendido exitosamente"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def convertir_en_venta(self, puja_uid: int) -> None:
        try:
            ServicioLibroDiario(self.__db).convertir_en_venta(puja_uid)
            self._responder_bien_con(self.VENTA_EXITOSA)
        except Exception as err:
            self._responder_mal_con(str(err))

    def listar_compras_de(self, pujador_uid: int) -> None:
        try:
            compras = ServicioLibroDiario(self.__db).listar_compras_de(pujador_uid)
            self._responder_bien_serializando_lista(compras)
        except Exception as err:
            self._responder_mal_con(str(err))

    def registrar_venta_en(self, lote_uid: int) -> None:
        try:
            venta = ServicioLibroDiario(self.__db).registrar_venta_en(lote_uid)
            if venta is None:
                self._responder_bien_con(self.LOTE_DESIERTO)
            else:
                self._responder_bien_con_numero("precio_final", venta.obtener_precio_final())
        except Exception as err:
            self._responder_mal_con(str(err))
