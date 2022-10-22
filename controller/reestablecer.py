from model.usuarios import Usuarios, Usuario


class EmailSender:
    def enviar_mail_a(self, usuario: Usuario):
        pass


class RealEmailSender(EmailSender):
    def enviar_mail_a(self, usuario: Usuario):
        # codigo para enviar mail
        pass


class ReestablecerController:
    def __init__(self, db: Usuarios, email: str, sender: EmailSender = RealEmailSender()):
        usuario = db.buscar_por_email(email)
        if usuario:
            sender.enviar_mail_a(usuario)

        self.__respuesta = { "status": "ok", "mensaje": "Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta" }

    def obtener_respuesta(self):
        return self.__respuesta
