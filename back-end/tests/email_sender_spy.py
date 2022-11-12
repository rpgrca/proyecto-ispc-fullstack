from model.usuarios import Usuario
from services.email_sender import EmailSender


class EmailSenderSpy(EmailSender):
    def __init__(self):
        self.__enviado = False
        self.__mensaje = ""

    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        self.__enviado = True
        self.__mensaje = mensaje

    def envio_mail(self) -> bool:
        return self.__enviado

    def mensaje_enviado(self) -> str:
        return self.__mensaje
