# subasta.py
#
# cambiar_orden(articulo, orden)
# pujar(pujador, monto)
# listar_pujas()

from datetime import date
from controller.controller import Controller
from model.database import BaseDeDatos


class SubastaController(Controller):
    SIN_TITULO = "No se puede crear una subasta sin titulo"
    SIN_DESCRIPCION = "No se puede crear una subasta sin descripcion"
    SIN_IMAGEN = "No se puede crear una subasta sin imagen"
    SIN_FECHA = "No se puede crear una subasta sin fecha"
    LOTE_SIN_SUBASTA = "No se puede agregar un lote sin subasta"
    ARTICULO_NULO_EN_SUBASTA = "No se puede agregar un articulo nulo a una subasta"
    LOTE_SUBASTA_INEXISTENTE = "No se puede agregar un lote a una subasta inexistente"
    ARTICULO_INEXISTENTE = "No se puede agregar un articulo inexistente a una subasta"
    LOTE_AGREGADO = "El lote ha sido agregado correctamente"
    BUSCAR_SIN_SUBASTA = "No se puede buscar un lote sin subasta"
    SUBASTA_INEXISTENTE = "No se puede subastar un lote de una subasta inexistente"
    LOTE_INEXISTENTE = "No existe tal lote"
    CONTAR_SIN_SUBASTA = "No se puede contar lotes sin subasta"
    CONTAR_SUBASTA_INEXISTENTE = "No se puede contar lotes de una subasta inexistente"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> None:
        if not self._verificar(titulo, self.SIN_TITULO) or \
           not self._verificar(descripcion, self.SIN_DESCRIPCION) or \
           not self._verificar(imagen, self.SIN_IMAGEN) or \
           not self._verificar(fecha, self.SIN_FECHA):
            return

        subasta = self.__db.Subastas.crear(titulo, descripcion, imagen, fecha)
        self._responder_bien_incluyendo_id(f"La subasta ha sido agendada para {str(fecha)}", subasta.obtener_uid())

    def agregar_lote(self, subasta_uid: int, articulo_uid: str, base: int) -> None:
        if not self._verificar(subasta_uid, self.LOTE_SIN_SUBASTA) or \
           not self._verificar(articulo_uid, self.ARTICULO_NULO_EN_SUBASTA):
            return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, self.LOTE_SUBASTA_INEXISTENTE):
            return

        articulo = self.__db.Articulos.buscar_por_uid(articulo_uid)
        if not self._verificar(articulo, self.ARTICULO_INEXISTENTE):
            return

        subasta.agregar_lote(articulo, base)
        self._responder_bien_con(self.LOTE_AGREGADO)

    def obtener_lote(self, subasta_uid: int, orden: int) -> None:
        if not self._verificar(subasta_uid, self.BUSCAR_SIN_SUBASTA):
            return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, self.SUBASTA_INEXISTENTE):
            return

        if orden < 1 or orden > subasta.contar_lotes():
            self._responder_mal_con(self.LOTE_INEXISTENTE)
            return

        lote = subasta.obtener_lote(orden - 1)
        self._responder_bien_serializando(lote)

    def contar_lotes(self, subasta_uid: int) -> None:
        if not self._verificar(subasta_uid, self.CONTAR_SIN_SUBASTA):
            return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, self.CONTAR_SUBASTA_INEXISTENTE):
            return

        self._responder_bien_con_numero("total", subasta.contar_lotes())
