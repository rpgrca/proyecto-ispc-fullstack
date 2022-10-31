from controller.controlador import Controlador
from services.login import ServicioLogin
from services.email_sender import EmailSender, RealEmailSender
from model.database import BaseDeDatos


class ControladorLogin(Controlador):
    RECORDATORIO_EXITOSO = "Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def login(self, usuario: str, clave: str):
        try:
            ServicioLogin(self.__db).login(usuario, clave)
            self._responder_bien_con(f"Bienvenido/a, {usuario}!")
        except Exception as err:
            self._responder_mal_con(str(err))

    def recordar(self, email: str, sender: EmailSender = RealEmailSender()):
        try:
            ServicioLogin(self.__db).recordar(email, sender)
            self._responder_bien_con(self.RECORDATORIO_EXITOSO)
        except Exception as err:
            self._responder_mal_con(str(err))
