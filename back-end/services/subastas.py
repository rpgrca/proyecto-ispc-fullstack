from datetime import date
from .servicio import Servicio
from model.database import BaseDeDatos


class ServicioSubasta(Servicio):
    SIN_TITULO = "No se puede crear una subasta sin titulo"
    SIN_DESCRIPCION = "No se puede crear una subasta sin descripcion"
    SIN_IMAGEN = "No se puede crear una subasta sin imagen"
    SIN_FECHA = "No se puede crear una subasta sin fecha"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> int:
        self._throw_if_invalid(titulo, self.SIN_TITULO)
        self._throw_if_invalid(descripcion, self.SIN_DESCRIPCION)
        self._throw_if_invalid(imagen, self.SIN_IMAGEN)
        self._throw_if_invalid(fecha, self.SIN_FECHA)

        subasta = self.__db.Subastas.crear(titulo, descripcion, imagen, fecha)
        return subasta.obtener_uid()
