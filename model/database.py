from model.subastas import Subastas
from model.usuarios import Usuarios
from model.articulos import Articulos


class BaseDeDatos:
    def __init__(self, usuarios: Usuarios, subastas: Subastas, articulos: Articulos):
        self.__usuarios = usuarios
        self.__subastas = subastas
        self.__articulos = articulos

    @property
    def Usuarios(self) -> Usuarios:
        return self.__usuarios

    @property
    def Subastas(self) -> Subastas:
        return self.__subastas

    @property
    def Articulos(self) -> Articulos:
        return self.__articulos
