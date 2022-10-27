from abc import ABC, abstractmethod
from datetime import date


class Subasta:
    def __init__(self, uid: int, titulo: str, descripcion: str, imagen: str, fecha: date):
        self.__uid = uid
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__imagen = imagen
        self.__fecha = fecha

    def obtener_uid(self) -> int:
        return self.__uid

    def obtener_titulo(self) -> str:
        return self.__titulo

    def obtener_imagen(self) -> str:
        return self.__imagen

    def obtener_descripcion(self) -> str:
        return self.__descripcion

    def obtener_fecha(self) -> date:
        return self.__fecha


class Subastas(ABC):
    @abstractmethod
    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        pass

    @abstractmethod
    def buscar_por_uid(self, uid: int) -> Subasta:
        pass
