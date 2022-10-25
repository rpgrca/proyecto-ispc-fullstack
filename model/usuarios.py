from datetime import date
from model.tipo_usuario import TipoDeUsuario


class Usuario:
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__usuario = usuario
        self.__clave = clave
        self.__nacimiento = nacimiento
        self.__tipo = tipo

    def __str__(self):
        return self.__usuario
    
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
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)


class Consignatario(Usuario):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)


class Martillero(Usuario):
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        super().__init__(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Martillero)


class Usuarios:
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario) -> None:
        pass
    
    def existe(self, usuario: str) -> bool:
        pass
    
    def buscar(self, usuario: str, clave: str) -> Usuario:
        pass
    
    def buscar_por_email(self, email: str, clave: str) -> Usuario:
        pass
    
    def existe_con_mail(self, email: str) -> bool:
        pass


class UsuariosFactory:
    @staticmethod
    def crear(nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario):
        if tipo == TipoDeUsuario.Consignatario:
            return Consignatario(nombre, apellido, email, usuario, clave, nacimiento)
        elif tipo == TipoDeUsuario.Pujador:
            return Pujador(nombre, apellido, email, usuario, clave, nacimiento)
        else:
            return Martillero(nombre, apellido, email, usuario, clave, nacimiento)