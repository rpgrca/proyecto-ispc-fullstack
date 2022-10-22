from model.usuarios import Usuarios

class LoginController:
    def __init__(self, db: Usuarios, usuario: str, clave: str):
        if not usuario:
            self.__mensaje_error_por_dato_faltante("usuario")
            return
        
        if not clave:
            self.__mensaje_error_por_dato_faltante("clave")
            return

        self.__respuesta = { "status": "error", "mensaje": "Usuario o contraseña inválida" }

        usuario = db.buscar(usuario, clave)
        if usuario:
            self.__respuesta = { "status": "ok", "mensaje": f"Bienvenido/a, {usuario}!" }

    def __mensaje_error_por_dato_faltante(self, atributo) -> None:
        self.__respuesta = { 'status': 'error', "mensaje": f"No se puede ingresar sin {atributo}" }

    def obtener_respuesta(self) -> dict[str, str]:
        return self.__respuesta