from datetime import date
from controller.controlador import Controlador
from services.usuarios import ServicioUsuario
from model.tipo_usuario import TipoDeUsuario
from model.database import BaseDeDatos


class ControladorUsuario(Controlador):
    CUENTA_CREADA = "La cuenta ha sido creada correctamente"
    CUENTA_ACTUALIZADA = "La cuenta ha sido actualizada correctamente"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        try:
            ServicioUsuario(self.__db).agregar(nombre, apellido, email, usuario, clave, nacimiento, tipo)
            self._responder_bien_con(self.CUENTA_CREADA)
        except Exception as err:
            self._responder_mal_con(str(err))

    def actualizar(self, usuario_uid: int, usuario: str, email: str, clave: str) -> None:
        try:
            ServicioUsuario(self.__db).actualizar(usuario_uid, usuario, email, clave)
            self._responder_bien_con(self.CUENTA_ACTUALIZADA)
        except Exception as err:
            self._responder_mal_con(str(err))
