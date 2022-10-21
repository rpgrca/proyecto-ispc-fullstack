from model.usuarios import Usuarios

class LoginController:
    def __init__(self, db: Usuarios, usuario: str, clave: str):
        self.__usuario = usuario
        self.__clave = clave
        self.__response = { "status": "error", "mensaje": "Usuario o contraseña inválida" }

        usuario = db.buscar(usuario, clave)
        if usuario:
            self.__response = { "status": "ok", "mensaje": f"Bienvenido/a, {usuario}!" }

    def obtener_respuesta(self):
        return self.__response
