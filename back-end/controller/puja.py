from controller.controlador import Controlador
from services.pujas import ServicioPuja
from model.database import BaseDeDatos


class ControladorPuja(Controlador):
    PUJA_REALIZADA = "Puja realizada con éxito"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, lote_uid: int, pujador_uid: int, monto: int) -> None:
        try:
            ServicioPuja(self.__db).agregar(lote_uid, pujador_uid, monto)
            self._responder_bien_con(self.PUJA_REALIZADA)
        except Exception as err:
            self._responder_mal_con(str(err))

    def listar(self, lote_uid: int) -> None:
        try:
            pujas = ServicioPuja(self.__db).listar(lote_uid)
            self._responder_bien_serializando_lista(pujas)
        except Exception as err:
            self._responder_mal_con(str(err))
