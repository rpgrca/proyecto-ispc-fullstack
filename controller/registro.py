from datetime import date
from controller.usuario import ServicioUsuario
from model.database import BaseDeDatos
from model.tipo_usuario import TipoDeUsuario


class ControladorRegistro(ServicioUsuario):
    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)
