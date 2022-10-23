from datetime import date
import uuid

from model.lotes import Lote
from model.articulos import Articulo


class Subasta:
    def __init__(self, uid: uuid.UUID, titulo: str, descripcion: str, imagen: str, fecha: date):
        self.__uid = uid
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__imagen = imagen
        self.__fecha = fecha
        self.__lotes = []
        
    def obtener_uid(self):
        return self.__uid

    def agregar(self, articulo: Articulo, base: float):
        lote = Lote(articulo, base, len(self.__lotes) + 1)
        self.__lotes.append(lote)

    def obtener_lote(self, orden: int):
        return self.__lotes[orden]


class Subastas:
    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        pass
    
    def buscar_por_uid(self, uid: uuid.UUID) -> Subasta:
        pass