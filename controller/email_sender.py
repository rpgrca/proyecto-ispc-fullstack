from model.usuarios import Usuario


class EmailSender:
    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        pass


class RealEmailSender(EmailSender):
    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        # codigo para enviar mail
        pass