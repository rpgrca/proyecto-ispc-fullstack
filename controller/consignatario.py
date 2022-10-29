from controller.usuario import ControladorUsuario
from model.database import BaseDeDatos
from model.usuarios import TipoDeUsuario


class ControladorConsignatario(ControladorUsuario):
    def __init__(self, db: BaseDeDatos):
        super().__init__(db)

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().agregar(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)
