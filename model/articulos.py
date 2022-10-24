# articulos.py
#
# - crear(titulo, descripcion, valuacion, consignatario)
# - listar()
# - listar_para(consignatario)

import uuid
from model.serialization import Serializable

class Articulo(Serializable):
    def __init__(self, uid: uuid.UUID):
        self.__uid = uid

    def obtener_uid(self) -> uuid.UUID:
        return self.__uid

    def serialize(self):
        return { }
    
    
class Articulos:
    def agregar(self, articulo_uid: uuid.UUID):
        pass

    def buscar_por_uid(self, articulo_uid: uuid.UUID) -> Articulo:
        pass