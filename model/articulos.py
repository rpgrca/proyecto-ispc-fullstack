# articulos.py
#
# - crear(titulo, descripcion, valuacion, consignatario)
# - listar()
# - listar_para(consignatario)
from model.serialization import Serializable


class Articulo(Serializable):
    def __init__(self, uid: int):
        self.__uid = uid

    def obtener_uid(self) -> int:
        return self.__uid

    def serialize(self):
        return {}


class Articulos:
    def agregar(self, articulo_uid: int):
        pass

    def buscar_por_uid(self, articulo_uid: int) -> Articulo:
        pass
