from controller.controlador import Controlador
from services.articulos import ServicioArticulos
from model.database import BaseDeDatos


class ControladorArticulo(Controlador):
    ARTICULO_CREADO = "El artículo ha sido creado correctamente"
    ARTICULO_BORRADO = "El artículo ha sido borrado correctamente"
    ARTICULO_ACTUALIZADO = "El artículo ha sido actualizado correctamente"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, titulo: str, descripcion: str, valuacion: int, consignatario_uid: int) -> None:
        try:
            ServicioArticulos(self.__db).agregar(titulo, descripcion, valuacion, consignatario_uid)
            self._responder_bien_con(self.ARTICULO_CREADO)
        except Exception as err:
            self._responder_mal_con(str(err))

    def buscar_por_uid(self, uid: int) -> None:
        try:
            articulo = ServicioArticulos(self.__db).buscar_por_uid(uid)
            self._responder_bien_serializando_item(articulo)
        except Exception as err:
            self._responder_mal_con(str(err))

    def listar_articulos_propiedad_de(self, consignatario_uid: int) -> None:
        try:
            articulos = ServicioArticulos(self.__db).listar_articulos_propiedad_de(consignatario_uid)
            self._responder_bien_serializando_lista(articulos)
        except Exception as err:
            self._responder_mal_con(str(err))

    def contar(self) -> None:
        try:
            total = ServicioArticulos(self.__db).contar()
            self._responder_bien_con_numero("total", total)
        except Exception as err:
            self._responder_mal_con(str(err))

    def listar(self) -> None:
        try:
            lista = ServicioArticulos(self.__db).listar()
            self._responder_bien_serializando_lista(lista)
        except Exception as err:
            self._responder_mal_con(str(err))

    def borrar(self, uid: int) -> None:
        try:
            ServicioArticulos(self.__db).borrar(uid)
            self._responder_bien_con(self.ARTICULO_BORRADO)
        except Exception as err:
            self._responder_mal_con(str(err))

    def actualizar(self, uid: int, titulo: str, descripcion: str, valuacion: int, consignatario_uid: int) -> None:
        try:
            ServicioArticulos(self.__db).actualizar(uid, titulo, descripcion, valuacion, consignatario_uid)
            self._responder_bien_con(self.ARTICULO_ACTUALIZADO)
        except Exception as err:
            self._responder_mal_con(str(err))
