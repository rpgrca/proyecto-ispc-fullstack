from datetime import date
from controller.controlador import Controlador
from services.subastas import ServicioSubasta
from model.database import BaseDeDatos


class ControladorSubasta(Controlador):
    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> None:
        try:
            uid = ServicioSubasta(self.__db).crear(titulo, descripcion, imagen, fecha)
            self._responder_bien_incluyendo_id(f"La subasta ha sido agendada para {str(fecha)}", uid)
        except Exception as err:
            self._responder_mal_con(str(err))
