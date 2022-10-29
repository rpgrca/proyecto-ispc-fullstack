from controller.controlador import Controlador
from services.articulos import ServicioArticulos
from model.database import BaseDeDatos


class ControladorArticulo(Controlador):
    ARTICULO_CREADO = "El artículo ha sido creado correctamente"

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
