from datetime import date


class Subasta:
    def __init__(self, titulo: str, descripcion: str, imagen: str, fecha: date):
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__imagen = imagen
        self.__fecha = fecha
        self.__lotes = []


class Subastas:
    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date):
        pass