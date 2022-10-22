from controller.controller import Controller
from model.usuarios import Usuarios, Usuario

class EmailSender:
    def enviar_mail_a(self, usuario: Usuario) -> None:
        pass


class RealEmailSender(EmailSender):
    def enviar_mail_a(self, usuario: Usuario) -> None:
        # codigo para enviar mail
        pass


class ReestablecerController(Controller):
    def __init__(self, db: Usuarios, email: str, sender: EmailSender = RealEmailSender()):
        usuario = db.buscar_por_email(email)
        if usuario:
            sender.enviar_mail_a(usuario)

        self._responder_bien_con("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta")