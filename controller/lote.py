from controller.servicio import Servicio
from controller.controlador import Controller
from model.database import BaseDeDatos
from model.lotes import Lote


class ControladorLote(Controller):
    LOTE_AGREGADO = "El lote ha sido agregado correctamente"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, subasta_uid: int, articulo_uid: str, base: int):
        try:
            ServicioLote(self.__db).agregar(subasta_uid, articulo_uid, base)
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


class ServicioLote(Servicio):
    LOTE_SIN_SUBASTA = "No se puede agregar un lote sin subasta"
    ARTICULO_NULO_EN_SUBASTA = "No se puede agregar un articulo nulo a una subasta"
    LOTE_SUBASTA_INEXISTENTE = "No se puede agregar un lote a una subasta inexistente"
    ARTICULO_INEXISTENTE = "No se puede agregar un articulo inexistente a una subasta"
    BUSCAR_SIN_SUBASTA = "No se puede buscar un lote sin subasta"
    CONTAR_SUBASTA_INEXISTENTE = "No se puede contar lotes de una subasta inexistente"
    CONTAR_SIN_SUBASTA = "No se puede contar lotes sin subasta"
    SUBASTA_INEXISTENTE = "No se puede subastar un lote de una subasta inexistente"
    LOTE_INEXISTENTE = "No existe tal lote"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, subasta_uid: int, articulo_uid: str, base: int) -> None:
        self._throw_if_invalid(subasta_uid, self.LOTE_SIN_SUBASTA)
        self._throw_if_invalid(articulo_uid, self.ARTICULO_NULO_EN_SUBASTA)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.LOTE_SUBASTA_INEXISTENTE)

        articulo = self.__db.Articulos.buscar_por_uid(articulo_uid)
        self._throw_if_invalid(articulo, self.ARTICULO_INEXISTENTE)

        self.__db.Lotes.agregar(subasta, articulo, base, self.__db.Lotes.contar_lotes(subasta) + 1)


    def contar_lotes_en(self, subasta_uid: int) -> int:
        self._throw_if_invalid(subasta_uid, self.CONTAR_SIN_SUBASTA)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.CONTAR_SUBASTA_INEXISTENTE)

        return self.__db.Lotes.contar_lotes(subasta)


    def obtener(self, subasta_uid: int, orden: int) -> Lote:
        self._throw_if_invalid(subasta_uid, self.BUSCAR_SIN_SUBASTA)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.SUBASTA_INEXISTENTE)

        if orden < 1 or orden > self.__db.Lotes.contar_lotes(subasta):
            self._throw(self.LOTE_INEXISTENTE)

        return self.__db.Lotes.obtener(subasta, orden)
