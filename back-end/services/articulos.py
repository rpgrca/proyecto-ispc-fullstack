from .servicio import Servicio
from model.database import BaseDeDatos
from model.articulos import Articulo


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
    BORRAR_ARTICULO_INVALIDO = "No se puede borrar artículo inválido"
    BORRAR_ARTICULO_INEXISTENTE = "No se puede borrar artículo inexistente"
    BORRAR_ARTICULO_EN_LOTE = "No se puede borrar un artículo que pertenece a un lote"
    ACTUALIZANDO_ARTICULO_INEXISTENTE = "No se puede actualizar un artículo inexistente"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, titulo: str, descripcion: str, valuacion: int, consignatario_uid: int) -> None:
        self._throw_if_invalid(titulo, self.TITULO_INVALIDO)
        self._throw_if_invalid(descripcion, self.DESCRIPCION_INVALIDA)
        self._throw_if_not_positive(valuacion, self.VALUACION_INVALIDA)
        self._throw_if_not_positive(consignatario_uid, self.CONSIGNATARIO_INVALIDO)

        consignatario = self.__db.Usuarios.buscar_consignatario_por_uid(consignatario_uid)
        self._throw_if_invalid(consignatario, self.CONSIGNATARIO_INEXISTENTE)

        self.__db.Articulos.crear(titulo, descripcion, valuacion, consignatario)

    def buscar_por_uid(self, uid: int) -> Articulo:
        self._throw_if_not_positive(uid, self.UID_INVALIDO)
        articulo = self.__db.Articulos.buscar_por_uid(uid)
        self._throw_if_invalid(articulo, self.ARTICULO_INEXISTENTE)

        return articulo

    def listar_articulos_propiedad_de(self, consignatario_uid: int) -> list[Articulo]:
        self._throw_if_not_positive(consignatario_uid, self.LISTAR_CON_CONSIGNATARIO_INVALIDO)

        consignatario = self.__db.Usuarios.buscar_consignatario_por_uid(consignatario_uid)
        self._throw_if_invalid(consignatario, self.LISTAR_CON_CONSIGNATARIO_INEXISTENTE)

        return self.__db.Articulos.listar_articulos_propiedad_de(consignatario)

    def contar(self) -> int:
        return self.__db.Articulos.contar()

    def listar(self) -> list[Articulo]:
        return self.__db.Articulos.listar()

    def borrar(self, uid: int) -> None:
        self._throw_if_not_positive(uid, self.BORRAR_ARTICULO_INVALIDO)

        articulo = self.__db.Articulos.buscar_por_uid(uid)
        self._throw_if_invalid(articulo, self.BORRAR_ARTICULO_INEXISTENTE)

        if self.__db.Lotes.existe_con_articulo(articulo):
            self._throw(self.BORRAR_ARTICULO_EN_LOTE)

        self.__db.Articulos.borrar(uid)

    def actualizar(self, uid: int, titulo: str, descripcion: str, valuacion: str, consignatario_uid: int) -> None:
        self._throw_if_not_positive(uid, self.UID_INVALIDO)
        self._throw_if_not_positive(consignatario_uid, self.CONSIGNATARIO_INVALIDO)

        self._throw_if_invalid(titulo, self.TITULO_INVALIDO)
        self._throw_if_invalid(descripcion, self.DESCRIPCION_INVALIDA)
        self._throw_if_not_positive(valuacion, self.VALUACION_INVALIDA)

        articulo = self.__db.Articulos.buscar_por_uid(uid)
        self._throw_if_invalid(articulo, self.ACTUALIZANDO_ARTICULO_INEXISTENTE)

        consignatario = self.__db.Usuarios.buscar_consignatario_por_uid(consignatario_uid)
        self._throw_if_invalid(consignatario, self.CONSIGNATARIO_INEXISTENTE)

        self.__db.Articulos.actualizar(articulo, titulo, descripcion, valuacion, consignatario)
