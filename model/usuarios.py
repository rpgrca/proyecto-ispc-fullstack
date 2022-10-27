from datetime import date
from model.tipo_usuario import TipoDeUsuario


class Usuario:
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                 tipo: TipoDeUsuario):
        self.__uid = uid
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__usuario = usuario
        self.__clave = clave
        self.__nacimiento = nacimiento
        self.__tipo = tipo

    def __str__(self):
        return self.__usuario

    def obtener_uid(self) -> int:
        return self.__uid

    def obtener_clave(self) -> str:
        return self.__clave

    def obtener_nombre(self) -> str:
        return self.__nombre

    def obtener_apellido(self) -> str:
        return self.__apellido

    def obtener_email(self) -> str:
        return self.__email

    def obtener_usuario(self) -> str:
        return self.__usuario

    def obtener_nacimiento(self) -> date:
        return self.__nacimiento


class Pujador(Usuario):
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(uid, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)


class Consignatario(Usuario):
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(uid, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)


class Martillero(Usuario):
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(uid, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Martillero)


class Usuarios:
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        raise NotImplementedError()

    def existe(self, usuario: str) -> bool:
        raise NotImplementedError()

    def existe_con_mail(self, email: str) -> bool:
        raise NotImplementedError()

    def buscar(self, usuario: str, clave: str) -> Usuario:
        raise NotImplementedError()

    def buscar_por_email(self, email: str, clave: str) -> Usuario:
        raise NotImplementedError()

    def buscar_pujador_por_uid(self, uid: int) -> Pujador:
        raise NotImplementedError()


class UsuariosFactory:
    @staticmethod
    def crear(uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
              tipo: TipoDeUsuario):
        if tipo == TipoDeUsuario.Consignatario:
            return Consignatario(uid, nombre, apellido, email, usuario, clave, nacimiento)
        elif tipo == TipoDeUsuario.Pujador:
            return Pujador(uid, nombre, apellido, email, usuario, clave, nacimiento)
        else:
            return Martillero(uid, nombre, apellido, email, usuario, clave, nacimiento)
