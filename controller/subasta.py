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

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> None:
        if not self._verificar(titulo, self.SIN_TITULO) or \
           not self._verificar(descripcion, self.SIN_DESCRIPCION) or \
           not self._verificar(imagen, self.SIN_IMAGEN) or \
           not self._verificar(fecha, self.SIN_FECHA):
            return

        subasta = self.__db.Subastas.crear(titulo, descripcion, imagen, fecha)
        self._responder_bien_incluyendo_id(f"La subasta ha sido agendada para {str(fecha)}", subasta.obtener_uid())
