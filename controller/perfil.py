# perfil.py
#
# actualizar(usuario, email, password)
from controller.controlador import Controlador
from services.usuarios import ServicioUsuario
from model.database import BaseDeDatos


class ControladorPerfil(Controlador):
    PUJA_REALIZADA = "Perfil actualizado correctamente"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def actualizar(self, usuario_uid: int, usuario: str, email: str, password: str) -> None:
        try:
            ServicioUsuario(self.__db).actualizar(usuario_uid, usuario, email, password)
            self._responder_bien_con(self.PUJA_REALIZADA)
        except Exception as err:
            self._responder_mal_con(str(err))

    def listar(self, lote_uid: int) -> None:
        try:
            pujas = ServicioPuja(self.__db).listar(lote_uid)
            self._responder_bien_serializando_lista(pujas)
        except Exception as err:
            self._responder_mal_con(str(err))
