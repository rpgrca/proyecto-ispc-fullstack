from controller.usuario import UsuarioController
from model.database import BaseDeDatos
from model.usuarios import TipoDeUsuario


class ConsignatarioController(UsuarioController):
    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)
