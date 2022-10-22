from controller.usuario import UsuarioController
from model.usuarios import Usuarios, TipoDeUsuario

class RegistroController(UsuarioController):
    def __init__(self, db: Usuarios, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)