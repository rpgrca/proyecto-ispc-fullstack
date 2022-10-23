from model.articulos import Articulo
from model.serialization import Serializable


class Lote(Serializable):
    def __init__(self, articulo: Articulo, base: float, orden: int):
        self.__articulo = articulo
        self.__base = base
        self.__orden = orden

    def obtener_precio_base(self) -> float:
        return self.__base
    
    def obtener_orden(self) -> int:
        return self.__orden

    def serialize(self):
        return { "articulo": self.__articulo.serialize(), "base": self.__base, "orden": self.__orden }
