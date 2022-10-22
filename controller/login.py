from controller.controller import Controller
from model.usuarios import Usuarios

class LoginController(Controller):
    def __init__(self, db: Usuarios, usuario: str, clave: str):
        if not self._verificar(usuario, "No se puede ingresar sin usuario") or not self._verificar(clave, "No se puede ingresar sin clave"):
            return

        usuario = db.buscar(usuario, clave)
        if usuario:
            self._responder_bien_con(f"Bienvenido/a, {usuario}!")
        else:
            self._responder_mal_con("Usuario o contraseña inválida")