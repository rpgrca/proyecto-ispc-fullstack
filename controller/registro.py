from model.usuarios import Usuarios

class RegistroController:
    def __init__(self, db: Usuarios, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        if not nombre:
            self.__mensaje_error_por_dato_faltante("nombre")
            return

        if not apellido:
            self.__mensaje_error_por_dato_faltante("apellido")
            return

        if not email:
            self.__mensaje_error_por_dato_faltante("e-mail")
            return

        if not usuario:
            self.__mensaje_error_por_dato_faltante("usuario")
            return

        if not clave:
            self.__mensaje_error_por_dato_faltante("clave")
            return

        if not nacimiento:
            self.__mensaje_error_por_dato_faltante("nacimiento")
            return

        self.__resultado = { "status": "error", "mensaje": "La cuenta ya existe" }
        if not db.existe(usuario):
            if not db.buscar_por_email(email):
                db.agregar(nombre, apellido, email, usuario, clave, nacimiento)
                self.__resultado = { "status": "ok", "mensaje": "La cuenta ha sido creada correctamente, ya puede ingresar a su cuenta" }

    def __mensaje_error_por_dato_faltante(self, atributo) -> None:
        self.__resultado = { 'status': 'error', "mensaje": f"No se puede crear un usuario sin {atributo}" }

    def obtener_respuesta(self) -> dict[str, str]:
        return self.__resultado
