from controller.usuario import ServicioUsuario
from model.database import BaseDeDatos
from model.usuarios import TipoDeUsuario


class ServicioConsignatario(ServicioUsuario):
    def __init__(self, db: BaseDeDatos, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(db, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)
