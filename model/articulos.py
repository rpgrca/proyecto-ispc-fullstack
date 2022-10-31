# articulos.py
#
# - crear(titulo, descripcion, valuacion, consignatario)
# - listar()
# - listar_para(consignatario)
from abc import ABC, abstractmethod
from model.serialization import Serializable
from model.usuarios import Consignatario

# TODO: Cuando se complete articulo descomentar de los testeos


class Articulo(Serializable):
    def __init__(self, uid: int, titulo: str, descripcion: str, valuacion: int, consignatario: Consignatario):
        self.__uid = uid
        self.__consignatario = consignatario
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__valuacion = valuacion

    def obtener_uid(self) -> int:
        return self.__uid

    def obtener_consignatario_uid(self) -> int:
        return self.__consignatario.obtener_uid()

    def obtener_titulo(self) -> str:
        return self.__titulo

    def serialize(self):
        return {"id": self.__uid, "consignatario_id": self.__consignatario.obtener_uid(), "titulo": self.__titulo}


class Articulos(ABC):
    @abstractmethod
    def crear(self, titulo: str, descripcion: str, valuacion: int, consignatario: Consignatario) -> Articulo:
        pass

    @abstractmethod
    def buscar_por_uid(self, uid: int) -> Articulo:
        pass

    @abstractmethod
    def listar_articulos_propiedad_de(self, consignatario: Consignatario) -> list[Articulo]:
        pass

    @abstractmethod
    def contar(self) -> int:
        pass
