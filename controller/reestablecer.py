# reestablecer.py
#
# recuperar(email)
from fastapi import FastAPI
from model.usuarios import Usuarios

class ReestablecerController:
    def __init__(self, db: Usuarios, email: str):
        usuario = db.buscar_por_email(email)
        if usuario:
            self.enviar_mail_con_clave_a(usuario)

        self.__respuesta = { "status": "ok", "mensaje": "Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta" }

    def enviar_mail_con_clave_a(self, usuario):
        pass

    def obtener_respuesta(self):
        return self.__respuesta
