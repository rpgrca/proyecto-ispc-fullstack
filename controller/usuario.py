from controller.controller import Controller
from model.usuarios import Usuarios, TipoDeUsuario

class UsuarioController(Controller):
    def __init__(self, db: Usuarios, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario):
        if not self._verificar(nombre, "No se puede crear un usuario sin nombre") or \
           not self._verificar(apellido, "No se puede crear un usuario sin apellido") or \
           not self._verificar(email, "No se puede crear un usuario sin e-mail") or \
           not self._verificar(usuario, "No se puede crear un usuario sin usuario") or \
           not self._verificar(clave, "No se puede crear un usuario sin clave") or \
           not self._verificar(nacimiento, "No se puede crear un usuario sin fecha de nacimiento"):
           return

        self._responder_mal_con("La cuenta ya existe")
        if not db.existe(usuario):
            if not db.buscar_por_email(email):
                db.agregar(nombre, apellido, email, usuario, clave, nacimiento, tipo)
                self._responder_bien_con("La cuenta ha sido creada correctamente")