from datetime import date
from controller.usuario import ControladorUsuario
from model.database import BaseDeDatos
from model.tipo_usuario import TipoDeUsuario


class ControladorRegistro(ControladorUsuario):
    def __init__(self, db: BaseDeDatos):
        super().__init__(db)

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().agregar(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)
