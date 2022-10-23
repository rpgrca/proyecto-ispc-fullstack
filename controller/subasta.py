# subasta.py
#
# agregar_lote(articulo, base, orden)
# cambiar_orden(articulo, orden)
# comenzar()
# terminar()
# pujar(pujador, monto)
# listar_pujas()
# cerrar_lote()
# siguiente_lote()


import uuid
from datetime import date
from controller.controller import Controller
from model.database import BaseDeDatos
from model.lotes import Lote

class SubastaController(Controller):
    def __init__(self, db: BaseDeDatos):
        self.__db = db


    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> None:
        if not self._verificar(titulo, "No se puede crear una subasta sin titulo") or \
           not self._verificar(descripcion, "No se puede crear una subasta sin descripcion") or \
           not self._verificar(imagen, "No se puede crear una subasta sin imagen") or \
           not self._verificar(fecha, "No se puede crear una subasta sin fecha"):
           return

        self._responder_mal_con("No se pudo crear la subasta")
        subasta = self.__db.Subastas.crear(titulo, descripcion, imagen, fecha)
        if subasta is not None:
            self._responder_bien_incluyendo_id(f"La subasta ha sido agendada para {fecha}", subasta.obtener_uid())


    def agregar_lote(self, subasta_uid: uuid, lote: Lote):
        if not self._verificar(subasta_uid, "No se puede agregar un lote sin subasta") or \
           not self._verificar(lote, "No se puede agregar un lote nulo a una subasta"):
           return

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        if not self._verificar(subasta, "No se puede agregar un lote a una subasta inexistente"):
            return
            
        subasta.agregar(lote)
        self._responder_bien_con("El lote ha sido agregado correctamente")