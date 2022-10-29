from controller.controlador import Controlador
from services.login import ServicioLogin
from model.database import BaseDeDatos


class ControladorLogin(Controlador):
    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def login(self, usuario: str, clave: str):
        try:
            ServicioLogin(self.__db).login(usuario, clave)
            self._responder_bien_con(f"Bienvenido/a, {usuario}!")
        except Exception as err:
            self._responder_mal_con(str(err))
