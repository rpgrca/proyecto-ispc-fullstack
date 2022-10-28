from controller.servicio import Servicio
from model.database import BaseDeDatos


class ServicioLote(Servicio):
    LOTE_SIN_SUBASTA = "No se puede agregar un lote sin subasta"
    ARTICULO_NULO_EN_SUBASTA = "No se puede agregar un articulo nulo a una subasta"
    LOTE_SUBASTA_INEXISTENTE = "No se puede agregar un lote a una subasta inexistente"
    ARTICULO_INEXISTENTE = "No se puede agregar un articulo inexistente a una subasta"
    LOTE_AGREGADO = "El lote ha sido agregado correctamente"
    BUSCAR_SIN_SUBASTA = "No se puede buscar un lote sin subasta"
    CONTAR_SUBASTA_INEXISTENTE = "No se puede contar lotes de una subasta inexistente"
    CONTAR_SIN_SUBASTA = "No se puede contar lotes sin subasta"
    SUBASTA_INEXISTENTE = "No se puede subastar un lote de una subasta inexistente"
    LOTE_INEXISTENTE = "No existe tal lote"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, subasta_uid: int, articulo_uid: str, base: int) -> None:
        if not self._verificar(subasta_uid, self.LOTE_SIN_SUBASTA) or \
           not self._verificar(articulo_uid, self.ARTICULO_NULO_EN_SUBASTA):
            return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, self.LOTE_SUBASTA_INEXISTENTE):
            return

        articulo = self.__db.Articulos.buscar_por_uid(articulo_uid)
        if not self._verificar(articulo, self.ARTICULO_INEXISTENTE):
            return

        self.__db.Lotes.agregar(subasta, articulo, base, self.__db.Lotes.contar_lotes(subasta) + 1)
        self._responder_bien_con(self.LOTE_AGREGADO)

    def contar_lotes_en(self, subasta_uid: int) -> None:
        if not self._verificar(subasta_uid, self.CONTAR_SIN_SUBASTA):
            return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, self.CONTAR_SUBASTA_INEXISTENTE):
            return

        cuenta = self.__db.Lotes.contar_lotes(subasta)
        self._responder_bien_con_numero("total", cuenta)

    def obtener(self, subasta_uid: int, orden: int) -> None:
        if not self._verificar(subasta_uid, self.BUSCAR_SIN_SUBASTA):
            return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, self.SUBASTA_INEXISTENTE):
            return

        if orden < 1 or orden > self.__db.Lotes.contar_lotes(subasta):
            self._responder_mal_con(self.LOTE_INEXISTENTE)
            return

        lote = self.__db.Lotes.obtener(subasta, orden)
        self._responder_bien_serializando_item(lote)
