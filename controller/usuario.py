from datetime import date
from controller.controller import Controller
from model.tipo_usuario import TipoDeUsuario
from model.database import BaseDeDatos

class UsuarioController(Controller):
    SIN_NOMBRE = "No se puede crear un usuario sin nombre"
    SIN_APELLIDO = "No se puede crear un usuario sin apellido"
    SIN_EMAIL = "No se puede crear un usuario sin e-mail"
    SIN_USUARIO = "No se puede crear un usuario sin usuario"
    SIN_CLAVE = "No se puede crear un usuario sin clave"
    SIN_NACIMIENTO = "No se puede crear un usuario sin fecha de nacimiento"
    CUENTA_YA_EXISTE = "La cuenta ya existe"
    CUENTA_CREADA = "La cuenta ha sido creada correctamente"

    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date, tipo: TipoDeUsuario):
        if not self._verificar(nombre, self.SIN_NOMBRE) or \
           not self._verificar(apellido, self.SIN_APELLIDO) or \
           not self._verificar(email, self.SIN_EMAIL) or \
           not self._verificar(usuario, self.SIN_USUARIO) or \
           not self._verificar(clave, self.SIN_CLAVE) or \
           not self._verificar(nacimiento, self.SIN_NACIMIENTO):
           return

        self._responder_mal_con(self.CUENTA_YA_EXISTE)
        if not db.Usuarios.existe(usuario):
            if not db.Usuarios.buscar_por_email(email):
                db.Usuarios.agregar(nombre, apellido, email, usuario, clave, nacimiento, tipo)
                self._responder_bien_con(self.CUENTA_CREADA)


class ConsignatarioController(UsuarioController):
    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)


class PujadorController(UsuarioController):
    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)