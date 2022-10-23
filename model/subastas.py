from datetime import date
import uuid

from model.lotes import Lote


class Subasta:
    def __init__(self, uid: uuid, titulo: str, descripcion: str, imagen: str, fecha: date):
        self.__uid = uid
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__imagen = imagen
        self.__fecha = fecha
        self.__lotes = []
        
    def obtener_uid(self):
        return self.__uid

    def agregar(self, lote: Lote):
        self.__lotes.append(lote)


class Subastas:
    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        pass
    
    def buscar_por_uid(self, uid: uuid) -> Subasta:
        pass