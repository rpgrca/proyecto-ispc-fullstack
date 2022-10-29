# articulos.py
#
# - crear(titulo, descripcion, valuacion, consignatario)
# - listar()
# - listar_para(consignatario)
from abc import ABC, abstractmethod
from model.serialization import Serializable
from model.usuarios import Consignatario


class Articulo(Serializable):
    def __init__(self, uid: int):
        self.__uid = uid

    def obtener_uid(self) -> int:
        return self.__uid

    def serialize(self):
        return {}


class Articulos(ABC):
    @abstractmethod
    def agregar(self, uid: int):
        pass

    @abstractmethod
    def buscar_por_uid(self, uid: int) -> Articulo:
        pass

    @abstractmethod
    def listar_articulos_propiedad_de(self, consignatario: Consignatario) -> list[Articulo]:
        pass
