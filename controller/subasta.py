# subasta.py
#
# crear(titulo, descripcion, imagen, fecha)
# agregar_lote(articulo, base, orden)
# cambiar_orden(articulo, orden)
# comenzar()
# terminar()
# pujar(pujador, monto)
# listar_pujas()
# cerrar_lote()
# siguiente_lote()


from datetime import date
from controller.controller import Controller
from model.lotes import Lotes, Lote

class SubastaController(Controller):
    def __init__(self):
        pass

    def crear(self, db: Lotes, titulo: str, descripcion: str, imagen: str, fecha: date):
        