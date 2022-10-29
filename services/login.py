from .servicio import Servicio
from model.database import BaseDeDatos


class ServicioLogin(Servicio):
    SIN_USUARIO = "No se puede ingresar sin usuario"
    SIN_CLAVE = "No se puede ingresar sin clave"
    LOGIN_INVALIDO = "Usuario o contraseña inválida"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def login(self, usuario: str, clave: str):
        self._throw_if_invalid(usuario, self.SIN_USUARIO)
        self._throw_if_invalid(clave, self.SIN_CLAVE)

        usuario = self.__db.Usuarios.buscar(usuario, clave)
        self._throw_if_invalid(usuario, self.LOGIN_INVALIDO)
