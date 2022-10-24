# subasta.py
#
# cambiar_orden(articulo, orden)
# pujar(pujador, monto)
# listar_pujas()

import uuid
from datetime import date
from controller.controller import Controller
from model.database import BaseDeDatos
from model.articulos import Articulo

class SubastaController(Controller):
    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> None:
        if not self._verificar(titulo, "No se puede crear una subasta sin titulo") or \
           not self._verificar(descripcion, "No se puede crear una subasta sin descripcion") or \
           not self._verificar(imagen, "No se puede crear una subasta sin imagen") or \
           not self._verificar(fecha, "No se puede crear una subasta sin fecha"):
           return

        subasta = self.__db.Subastas.crear(titulo, descripcion, imagen, fecha)
        self._responder_bien_incluyendo_id(f"La subasta ha sido agendada para {fecha}", subasta.obtener_uid())

    def agregar_lote(self, subasta_uid: str, articulo_uid: str, base: float) -> None:
        if not self._verificar(subasta_uid, "No se puede agregar un lote sin subasta") or \
           not self._verificar(articulo_uid, "No se puede agregar un articulo nulo a una subasta"):
           return

        subasta = self.__db.Subastas.buscar_por_uid(uuid.UUID(subasta_uid))
        if not self._verificar(subasta, "No se puede agregar un lote a una subasta inexistente"):
            return

        articulo = self.__db.Articulos.buscar_por_uid(uuid.UUID(articulo_uid))
        if not self._verificar(articulo, "No se puede agregar un articulo inexistente a una subasta"):
            return

        subasta.agregar(articulo, base)
        self._responder_bien_con("El lote ha sido agregado correctamente")

    def obtener_lote(self, subasta_uid: str, orden: int) -> None:
        if not self._verificar(subasta_uid, "No se puede buscar un lote sin subasta"):
            return
        
        subasta = self.__db.Subastas.buscar_por_uid(uuid.UUID(subasta_uid))
        if not self._verificar(subasta, "No se puede subastar un lote de una subasta inexistente"):
            return

        if orden < 1 or orden > subasta.contar_lotes():
            self._responder_mal_con("No existe tal lote")
            return

        lote = subasta.obtener_lote(orden - 1)
        self._responder_bien_serializando(lote)

    def contar_lotes(self, subasta_uid: str) -> None:
        if not self._verificar(subasta_uid, "No se puede contar lotes sin subasta"):
            return

        subasta = self.__db.Subastas.buscar_por_uid(uuid.UUID(subasta_uid))
        if not self._verificar(subasta, "No se puede contar lotes de una subasta inexistente"):
            return

        self._responder_bien_con_numero("total", subasta.contar_lotes())