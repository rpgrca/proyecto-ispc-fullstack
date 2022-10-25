from datetime import date
from model.articulos import Articulo
from model.database import BaseDeDatos
from model.usuarios import Usuarios, Usuario, UsuariosFactory
from model.subastas import Subastas, Subasta
from model.articulos import Articulos
from model.tipo_usuario import TipoDeUsuario


class UsuariosFake(Usuarios):
    def __init__(self, usuarios):
        self.__usuarios = usuarios

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str, \
        tipo: TipoDeUsuario) -> None:
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
                return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"], \
                    registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_por_email(self, email: str) -> Usuario:
        registro = next(filter(lambda u: u["email"] == email, self.__usuarios.values()), None)
        if registro:
            return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"], \
                registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None


class SubastasFake(Subastas):
    def __init__(self, subastas: list):
        self.__subastas = subastas

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        subasta = Subasta(len(self.__subastas) + 1, titulo, descripcion, imagen, fecha)
        self.__subastas.append(subasta)
        return subasta

    def agregar_lote(self, subasta: Subasta, articulo: Articulo, base: int) -> None:
        subasta.agregar(articulo, base)

    def buscar_por_uid(self, uid: int) -> Subasta:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__subastas), None)

    def contar_lotes(self) -> int:
        return len(self.__subastas)


class ArticulosFake(Articulos):
    def __init__(self, articulos: list):
        self.__articulos = articulos

    def agregar(self, uid: int) -> None:
        self.__articulos.append(Articulo(uid))

    def buscar_por_uid(self, uid: int) -> Articulo:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__articulos), None)


class CreadorDeBasesDeDatosTemporales:
    def __init__(self):
        self.__usuarios = UsuariosFake({
            "Roberto": {
                "nombre": "Roberto",
                "apellido": "Perez",
                "usuario": "Roberto",
                "clave": "123456",
                "email": "roberto.carlos.alfonso@gmail.com",
                "nacimiento": 17/9/2000,
                "tipo": TipoDeUsuario.Pujador
            },
            "Martin": {
                "nombre": "Martin",
                "apellido": "Rodriguez",
                "usuario": "Martin",
                "clave": "654321",
                "email": "martin@gmail.com",
                "nacimiento": 10/5/2000,
                "tipo": TipoDeUsuario.Pujador
            },
            "Julia": {
                "nombre": "Julia",
                "apellido": "Gonzalez",
                "usuario": "Julia",
                "clave": "109283",
                "email": "julia@gmail.com",
                "nacimiento": 12/12/2000,
                "tipo": TipoDeUsuario.Pujador
            },
            "Estela": {
                "nombre": "Estela",
                "apellido": "Flores",
                "usuario": "Estela",
                "clave": "777777",
                "email": "estela@gmail.com",
                "nacimiento": 6/6/2000,
                "tipo": TipoDeUsuario.Consignatario
            },
            "Adrian": {
                "nombre": "Adrian",
                "apellido": "Acosta",
                "usuario": "Adrian",
                "clave": "martillero",
                "email": "martillero@gmail.com",
                "nacimiento": 4/20/2000,
                "tipo": TipoDeUsuario.Martillero
            }
        })
        self.__subastas = SubastasFake([Subasta(1, "Gran subasta!", "Nos vemos pronto!", "sofa.jpg", 17/10/2022)])
        self.__articulos = ArticulosFake([Articulo(1)])

    def con_usuarios(self, usuarios: Usuarios):
        self.__usuarios = usuarios
        return self

    def con_subastas(self, subastas: Subastas):
        self.__subastas = subastas
        return self

    def con_articulos(self, articulos: Articulos):
        self.__articulos = articulos
        return self

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos)
