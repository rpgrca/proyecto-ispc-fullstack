from services.lotes import ServicioLote
from controller.controlador import Controlador
from model.database import BaseDeDatos


class ControladorLote(Controlador):
    LOTE_AGREGADO = "El lote ha sido agregado correctamente"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, subasta_uid: int, articulo_uid: str, base: int, orden: int):
        try:
            ServicioLote(self.__db).agregar(subasta_uid, articulo_uid, base, orden)
            self._responder_bien_con(self.LOTE_AGREGADO)
        except Exception as err:
            self._responder_mal_con(str(err))

    def contar_lotes_en(self, subasta_uid: int):
        try:
            cuenta = ServicioLote(self.__db).contar_lotes_en(subasta_uid)
            self._responder_bien_con_numero("total", cuenta)
        except Exception as err:
            self._responder_mal_con(str(err))

    def obtener(self, subasta_uid: int, orden: int):
        try:
            lote = ServicioLote(self.__db).obtener(subasta_uid, orden)
            self._responder_bien_serializando_item(lote)
        except Exception as err:
            self._responder_mal_con(str(err))

    def listar(self, subasta_uid: int) -> None:
        try:
            catalogo = ServicioLote(self.__db).listar(subasta_uid)
            self._responder_bien_serializando_lista(catalogo)
        except Exception as err:
            self._responder_mal_con(str(err))
