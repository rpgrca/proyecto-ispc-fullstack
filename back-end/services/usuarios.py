from datetime import date
from .servicio import Servicio
from model.tipo_usuario import TipoDeUsuario
from model.database import BaseDeDatos
from services.email_sender import EmailSender


class ServicioUsuario(Servicio):
    SIN_NOMBRE = "No se puede crear un usuario sin nombre"
    SIN_APELLIDO = "No se puede crear un usuario sin apellido"
    SIN_EMAIL = "No se puede crear un usuario sin e-mail"
    SIN_USUARIO = "No se puede crear un usuario sin usuario"
    SIN_CLAVE = "No se puede crear un usuario sin clave"
    SIN_NACIMIENTO = "No se puede crear un usuario sin fecha de nacimiento"
    CUENTA_YA_EXISTE = "La cuenta ya existe"
    USUARIO_UID_INVALIDO = "No se puede actualizar un usuario inválido"
    USUARIO_INVALIDO = "No se puede utilizar un usuario inválido"
    EMAIL_INVALIDO = "No se puede utilizar un e-mail inválido"
    CLAVE_INVALIDA = "No se puede utilizar una clave inválida"
    USUARIO_INEXISTENTE = "No se puede actualizar un usuario inexistente"
    USUARIO_YA_EXISTE = "Nombre de usuario ya existe"
    CONTACTO_SIN_NOMBRE = "No se puede contactar al martillero sin nombre"
    CONTACTO_SIN_EMAIL = "No se puede contactar al martillero sin e-mail"
    CONTACTO_SIN_ASUNTO = "No se puede contactar al martillero sin asunto"
    CONTACTO_SIN_TEXTO = "No se puede contactar al martillero sin texto"
    MARTILLERO_INEXISTENTE = "No se puede enviar mensaje a ningún martillero por el momento"
    SENDER_INVALIDO = "No se puede contactar al martillero sin sender"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        self._throw_if_invalid(nombre, self.SIN_NOMBRE)
        self._throw_if_invalid(apellido, self.SIN_APELLIDO)
        self._throw_if_invalid(email, self.SIN_EMAIL)
        self._throw_if_invalid(usuario, self.SIN_USUARIO)
        self._throw_if_invalid(clave, self.SIN_CLAVE)
        self._throw_if_invalid(nacimiento, self.SIN_NACIMIENTO)

        self._throw_if_true(self.__db.Usuarios.existe(usuario), self.CUENTA_YA_EXISTE)
        self._throw_if_true(self.__db.Usuarios.buscar_por_email(email), self.CUENTA_YA_EXISTE)
        self.__db.Usuarios.agregar(nombre, apellido, email, usuario, clave, nacimiento, tipo)

    def actualizar(self, usuario_uid: int, usuario: str, email: str, clave: str) -> None:
        self._throw_if_not_positive(usuario_uid, self.USUARIO_UID_INVALIDO)
        self._throw_if_invalid(usuario, self.USUARIO_INVALIDO)
        self._throw_if_invalid(email, self.EMAIL_INVALIDO)
        self._throw_if_invalid(clave, self.CLAVE_INVALIDA)

        cuenta = self.__db.Usuarios.buscar_usuario_por_uid(usuario_uid)
        self._throw_if_invalid(cuenta, self.USUARIO_INEXISTENTE)

        if cuenta.obtener_usuario() != usuario and self.__db.Usuarios.existe(usuario):
            self._throw(self.USUARIO_YA_EXISTE)

        self.__db.Usuarios.actualizar(cuenta, usuario, email, clave)

    def contactar(self, nombre: str, email: str, asunto: str, texto: str, sender: EmailSender) -> None:
        self._throw_if_invalid(nombre, self.CONTACTO_SIN_NOMBRE)
        self._throw_if_invalid(email, self.CONTACTO_SIN_EMAIL)
        self._throw_if_invalid(asunto, self.CONTACTO_SIN_ASUNTO)
        self._throw_if_invalid(texto, self.CONTACTO_SIN_TEXTO)
        self._throw_if_invalid(sender, self.SENDER_INVALIDO)

        martillero = self.__db.Usuarios.buscar_martillero()
        self._throw_if_invalid(martillero, self.MARTILLERO_INEXISTENTE)

        sender.enviar_mail_a(martillero, f"{nombre} te envió un mail titulado {asunto}. {texto}. Responde a {email}")
