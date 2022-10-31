from model.usuarios import Usuario
from services.email_sender import EmailSender

class EmailSenderSpy(EmailSender):
    def __init__(self):
        self.__enviado = False

    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        self.__enviado = True

    def envio_mail(self) -> bool:
        return self.__enviado
