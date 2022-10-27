from controller.servicio import Servicio
from controller.email_sender import EmailSender, RealEmailSender
from model.database import BaseDeDatos


class ServicioController(Servicio):
    RECORDATORIO_EXITOSO = "Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta"

    def __init__(self, db: BaseDeDatos, email: str, sender: EmailSender = RealEmailSender()):
        super().__init__()
        usuario = db.Usuarios.buscar_por_email(email)
        if usuario:
            sender.enviar_mail_a(usuario, f"Recordatorio: Su clave es {usuario.obtener_clave()}")

        self._responder_bien_con(self.RECORDATORIO_EXITOSO)
