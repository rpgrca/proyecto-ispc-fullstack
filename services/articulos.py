from .servicio import Servicio
from model.database import BaseDeDatos
from model.articulos import Articulo
from model.usuarios import Consignatario

class ServicioArticulos(Servicio):
    UID_INVALIDO = "Artículo invalido"
    TITULO_INVALIDO = "No se puede crear un artículo con título inválido"
    DESCRIPCION_INVALIDA = "No se puede crear un artículo con descripción inválida"
    VALUACION_INVALIDA = "No se puede crear un artículo con valuación inválida"
    CONSIGNATARIO_INVALIDO = "No se puede crear un artículo con consignatario inválido"
    LISTAR_CON_CONSIGNATARIO_INVALIDO = "No se puede listar artículos de un consignatario inválido"
    CONSIGNATARIO_INEXISTENTE = "No se puede crear un artículo con un consignatario inexistente"
    LISTAR_CON_CONSIGNATARIO_INEXISTENTE = "No se puede listar artículos de un consignatario inexistente"
    ARTICULO_INEXISTENTE = "El artículo no existe"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, titulo: str, descripcion: str, valuacion: int, consignatario_uid: int) -> None:
        self._throw_if_invalid(titulo, self.TITULO_INVALIDO)
        self._throw_if_invalid(descripcion, self.DESCRIPCION_INVALIDA)
        self._throw_if_true(valuacion <= 0, self.VALUACION_INVALIDA)
        self._throw_if_true(consignatario_uid <= 0, self.CONSIGNATARIO_INVALIDO)

        consignatario = self.__db.Usuarios.buscar_consignatario_por_uid(consignatario_uid)
        self._throw_if_invalid(consignatario, self.CONSIGNATARIO_INEXISTENTE)

        self.__db.Articulos.agregar(self.__db.Articulos.contar() + 1)

    def buscar_por_uid(self, uid: int) -> Articulo:
        self._throw_if_true(uid <= 0, self.UID_INVALIDO)
        articulo = self.__db.Articulos.buscar_por_uid(uid)
        self._throw_if_invalid(articulo, self.ARTICULO_INEXISTENTE)

        return articulo

    def listar_articulos_propiedad_de(self, consignatario_uid: int) -> list[Articulo]:
        self._throw_if_true(consignatario_uid <= 0, self.LISTAR_CON_CONSIGNATARIO_INVALIDO)
        
        consignatario = self.__db.Usuarios.buscar_consignatario_por_uid(consignatario_uid)
        self._throw_if_invalid(consignatario, self.LISTAR_CON_CONSIGNATARIO_INEXISTENTE)

        return self.__db.Articulos.listar_articulos_propiedad_de(consignatario)
