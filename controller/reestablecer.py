from controller.controller import Controller
from controller.email_sender import EmailSender, RealEmailSender
from model.usuarios import Usuarios, Usuario

class ReestablecerController(Controller):
    def __init__(self, db: Usuarios, email: str, sender: EmailSender = RealEmailSender()):
        usuario = db.buscar_por_email(email)
        if usuario:
            sender.enviar_mail_a(usuario, f"Recordatorio: Su clave es {usuario.obtener_clave()}")

        self._responder_bien_con("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta")