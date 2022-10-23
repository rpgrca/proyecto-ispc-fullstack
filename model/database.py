from model.subastas import Subastas
from model.usuarios import Usuarios
from model.lotes import Lotes

class BaseDeDatos:
    def __init__(self, usuarios: Usuarios, lotes: Lotes, subastas: Subastas):
        self.__usuarios = usuarios
        self.__lotes = lotes
        self.__subastas = subastas

    @property
    def Usuarios(self) -> Usuarios:
        return self.__usuarios

    @property
    def Lotes(self) -> Lotes:
        return self.__lotes
    
    @property
    def Subastas(self) -> Subastas:
        return self.__subastas