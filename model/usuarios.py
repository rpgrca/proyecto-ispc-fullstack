from datetime import date
from abc import ABC, abstractmethod
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

    def obtener_tipo(self) -> TipoDeUsuario:
        return self.__tipo


class Pujador(Usuario):
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(uid, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)


class Consignatario(Usuario):
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(uid, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)


class Martillero(Usuario):
    def __init__(self, uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date):
        super().__init__(uid, nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Martillero)


class Usuarios(ABC):
    @staticmethod
    def crear(uid: int, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
              tipo: TipoDeUsuario) -> Usuario:
        # Si el metodo se llama desde MySQL a traves de un query el tipo llega como un numero, por eso
        # tengo que validar si tipo es el enum o el valor
        if tipo == TipoDeUsuario.Consignatario or tipo == TipoDeUsuario.Consignatario.value:
            return Consignatario(uid, nombre, apellido, email, usuario, clave, nacimiento)
        elif tipo == TipoDeUsuario.Pujador or tipo == TipoDeUsuario.Pujador.value:
            return Pujador(uid, nombre, apellido, email, usuario, clave, nacimiento)
        else:
            return Martillero(uid, nombre, apellido, email, usuario, clave, nacimiento)

    @abstractmethod
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: date,
                tipo: TipoDeUsuario) -> None:
        pass

    @abstractmethod
    def existe(self, usuario: str) -> bool:
        pass

    @abstractmethod
    def buscar(self, usuario: str, clave: str) -> Usuario:
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Usuario:
        pass

    @abstractmethod
    def buscar_pujador_por_uid(self, uid: int) -> Pujador:
        pass

    @abstractmethod
    def buscar_consignatario_por_uid(self, uid: int) -> Consignatario:
        pass

    @abstractmethod
    def buscar_usuario_por_uid(self, uid: int) -> Usuario:
        pass

    @abstractmethod
    def actualizar(self, cuenta: Usuario, usuario: str, email: str, clave: str) -> None:
        pass

    @abstractmethod
    def buscar_martillero(self) -> Martillero:
        pass
