from controller.controlador import Controlador
from services.lotes import ServicioLote
from model.database import BaseDeDatos


class ControladorCatalogo(Controlador):

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def listar(self, subasta_uid: int) -> None:
        try:
            catalogo = ServicioLote(self.__db).listar(subasta_uid)
            self._responder_bien_serializando_lista(catalogo)
        except Exception as err:
            self._responder_mal_con(str(err))
