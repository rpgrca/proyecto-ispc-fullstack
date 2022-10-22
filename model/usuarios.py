from enum import Enum


class TipoDeUsuario(Enum):
    Martillero = 1,
    Consignatario = 2,
    Pujador = 3


class Usuario:
    def __init__(self, usuario, clave):
        self.__usuario = usuario
        self.__clave = clave

    def __str__(self):
        return self.__usuario


class Usuarios:
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario) -> None:
        pass
    
    def existe(self, usuario: str) -> bool:
        pass
    
    def buscar(self, usuario: str, clave: str) -> Usuario:
        pass
    
    def existe_con_mail(self, email: str) -> bool:
        pass
    
    def encriptar(self, clave: str) -> str:
        pass


class UsuariosImplementadoConDiccionario(Usuarios):
    def __init__(self, usuarios):
        self.__usuarios = usuarios
        
    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, tipo: TipoDeUsuario) -> None:
        self.__usuarios[usuario] = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "usuario": usuario,
            "clave": clave,
            "nacimiento": nacimiento,
            "tipo": tipo.value
        }

    def existe(self, usuario: str) -> bool:
        return usuario in self.__usuarios

    def buscar(self, usuario: str, clave: str) -> Usuario:
        if usuario in self.__usuarios:
            if self.__usuarios[usuario]['clave'] == self.encriptar(clave):
                return Usuario(usuario, clave)

        return None

    def buscar_por_email(self, email: str) -> bool:
        return any(filter(lambda u: u['email'] == email, self.__usuarios.values()))

    def encriptar(self, clave: str) -> str:
        return clave
