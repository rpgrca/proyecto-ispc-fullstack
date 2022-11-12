from model.usuarios import Usuario
from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        pass


class RealEmailSender(EmailSender):
    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        """
        codigo para enviar mail al email del usuario
        """
