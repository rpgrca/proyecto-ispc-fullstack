from controller.controller import Controller
from model.database import BaseDeDatos


class LoginController(Controller):
    SIN_USUARIO = "No se puede ingresar sin usuario"
    SIN_CLAVE = "No se puede ingresar sin clave"
    LOGIN_INVALIDO = "Usuario o contraseña inválida"

    def __init__(self, db: BaseDeDatos, usuario: str, clave: str):
        super().__init__()
        if not self._verificar(usuario, self.SIN_USUARIO) or \
           not self._verificar(clave, self.SIN_CLAVE):
            return

        usuario = db.Usuarios.buscar(usuario, clave)
        if usuario:
            self._responder_bien_con(f"Bienvenido/a, {usuario}!")
        else:
            self._responder_mal_con(self.LOGIN_INVALIDO)
