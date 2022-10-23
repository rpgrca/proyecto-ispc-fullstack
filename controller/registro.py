from controller.usuario import UsuarioController
from model.database import BaseDeDatos
from model.tipo_usuario import TipoDeUsuario

class RegistroController(UsuarioController):
    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)