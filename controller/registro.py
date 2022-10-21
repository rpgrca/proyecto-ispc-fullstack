from model.usuarios import Usuarios

class RegistroController:
    def __init__(self, db: Usuarios, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        if db.existe(usuario):
            self.__resultado = { "status": "error", "mensaje": "La cuenta ya existe" }
        else:
            db.agregar(nombre, apellido, email, usuario, clave, nacimiento)
            self.__resultado = { "status": "ok", "mensaje": "La cuenta ha sido creada correctamente, ya puede ingresar a su cuenta" }

    def obtener_respuesta(self):
        return self.__resultado
