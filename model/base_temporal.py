from datetime import date
from model.database import BaseDeDatos
from model.usuarios import Usuarios, Usuario, UsuariosFactory
from model.subastas import Subastas, Subasta
from model.tipo_usuario import TipoDeUsuario
from model.lotes import Lotes


class UsuariosFake(Usuarios):
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
            registro = self.__usuarios[usuario]
            if registro["clave"] == clave:
                return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"], registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_por_email(self, email: str) -> Usuario:
        registro = next(filter(lambda u: u["email"] == email, self.__usuarios.values()), None)
        if registro:
            return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"], registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None



class SubastasFake(Subastas):
    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date):
        return Subasta(titulo, descripcion, imagen, fecha)


class CreadorDeBasesDeDatosTemporales:
    def __init__(self):
        self.__usuarios = UsuariosFake({
            "Roberto": { "nombre": "Roberto", "apellido": "Perez", "usuario": "Roberto", "clave": "123456", "email": "roberto.carlos.alfonso@gmail.com", "nacimiento": 17/9/2000, "tipo": 3 },
            "Martin": { "nombre": "Martin", "apellido": "Rodriguez", "usuario": "Martin", "clave": "654321", "email": "martin@gmail.com", "nacimiento": 10/5/2000, "tipo": 3 },
            "Julia": { "nombre": "Julia", "apellido": "Gonzalez", "usuario": "Julia", "clave": "109283", "email": "julia@gmail.com", "nacimiento": 12/12/2000, "tipo": 3 },
            "Estela": { "nombre": "Estela", "apellido": "Flores", "usuario": "Estela", "clave": "777777", "email": "estela@gmail.com", "nacimiento": 6/6/2000, "tipo": 2 },
            "Adrian": { "nombre": "Adrian", "apellido": "Acosta", "usuario": "Adrian", "clave": "martillero", "email": "martillero@gmail.com", "nacimiento": 4/20/2000, "tipo": 1 }
        })
        self.__lotes = []
        self.__subastas = []
            
    def con_usuarios(self, usuarios: Usuarios):
        self.__usuarios = usuarios
        return self
    
    def con_lotes(self, lotes: Lotes):
        self.__lotes = lotes
        return self
    
    def con_subastas(self, subastas: Subastas):
        self.__subastas = subastas
        return self

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__lotes, self.__subastas)
