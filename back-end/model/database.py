from model.pujas import Pujas
from model.subastas import Subastas
from model.usuarios import Usuarios
from model.articulos import Articulos
from model.lotes import Lotes
from model.libro_diario import LibroDiario


class BaseDeDatos:
    def __init__(self, usuarios: Usuarios, subastas: Subastas, articulos: Articulos, lotes: Lotes, pujas: Pujas,
                 ventas: LibroDiario):
        self.__usuarios = usuarios
        self.__subastas = subastas
        self.__articulos = articulos
        self.__lotes = lotes
        self.__pujas = pujas
        self.__ventas = ventas

    @property
    def Usuarios(self) -> Usuarios:
        return self.__usuarios

    @property
    def Subastas(self) -> Subastas:
        return self.__subastas

    @property
    def Articulos(self) -> Articulos:
        return self.__articulos

    @property
    def Lotes(self) -> Lotes:
        return self.__lotes

    @property
    def Pujas(self) -> Pujas:
        return self.__pujas

    @property
    def Ventas(self) -> LibroDiario:
        return self.__ventas
