from datetime import date
from model.articulos import Articulo
from model.database import BaseDeDatos
from model.usuarios import Pujador, Usuarios, Usuario, UsuariosFactory
from model.subastas import Subastas, Subasta
from model.articulos import Articulos
from model.pujas import Puja
from model.tipo_usuario import TipoDeUsuario
from model.lotes import Lote, Lotes


class UsuariosEnMemoria(Usuarios):
    def __init__(self, usuarios):
        self.__id = 1
        self.__usuarios = usuarios

    def agregar(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str,
                tipo: TipoDeUsuario) -> None:
        self.__usuarios[usuario] = {
            "id": self.__id,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "usuario": usuario,
            "clave": clave,
            "nacimiento": nacimiento,
            "tipo": tipo.value
        }
        self.__id += 1

    def existe(self, usuario: str) -> bool:
        return usuario in self.__usuarios

    def existe_con_mail(self, email: str) -> bool:
        return any(filter(lambda u: u["email"] == email, self.__usuarios.values()))

    def buscar(self, usuario: str, clave: str) -> Usuario:
        if usuario in self.__usuarios:
            registro = self.__usuarios[usuario]
            if registro["clave"] == clave:
                return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"],
                                             registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_por_email(self, email: str) -> Usuario:
        registro = next(filter(lambda u: u["email"] == email, self.__usuarios.values()), None)
        if registro:
            return UsuariosFactory.crear(registro["nombre"], registro["apellido"], registro["email"],
                                         registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_pujador_por_uid(self, uid: int) -> Pujador:
        return next(filter(lambda u: u["id"] == uid and u["tipo_usuario"] == TipoDeUsuario.Pujador, self.__usuarios), None)


class SubastasEnMemoria(Subastas):
    def __init__(self, subastas: list):
        self.__subastas = subastas

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        subasta = Subasta(len(self.__subastas) + 1, titulo, descripcion, imagen, fecha)
        self.__subastas.append(subasta)
        return subasta

    def buscar_por_uid(self, uid: int) -> Subasta:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__subastas), None)


class ArticulosEnMemoria(Articulos):
    def __init__(self, articulos: list):
        self.__articulos = articulos

    def agregar(self, uid: int) -> None:
        self.__articulos.append(Articulo(uid))

    def buscar_por_uid(self, uid: int) -> Articulo:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__articulos), None)


class PujasEnMemoria:
    def __init__(self, pujas: list):
        self.__pujas = pujas

    def agregar(self, monto: int, pujador: Pujador, lote: Lote):
        self.__pujas.append(Puja(monto, pujador, lote))

    def buscar_por_monto(self, monto: int) -> Puja:
        pass


class LotesEnMemoria:
    def __init__(self, lotes: list):
        self.__lotes = lotes
        
    def agregar(self, subasta: Subasta, articulo: Articulo, base: int, orden: int):
        self.__lotes.append(Lote(subasta, articulo, base, orden))

    def contar_lotes(self, subasta: Subasta) -> int:
        return sum(1 if l.obtener_subasta_uid() == subasta.obtener_uid() else 0 for l in self.__lotes)
    
    def obtener(self, subasta: Subasta, orden: int) -> Lote:
        return next(l for l in self.__lotes if l.obtener_subasta_uid() == subasta.obtener_uid() and l.obtener_orden() == orden)

    def buscar_por_uid(self, lote_uid: int) -> Lote:
        return next(filter(lambda: l.obtener_uid() == lote_uid, self.__lotes))


class CreadorDeBasesDeDatosTemporales:
    def __init__(self):
        self.__usuarios = UsuariosEnMemoria({
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
        self.__subastas = SubastasEnMemoria([Subasta(1, "Gran subasta!", "Nos vemos pronto!", "sofa.jpg", 17/10/2022)])
        self.__articulos = ArticulosEnMemoria([Articulo(1)])
        self.__lotes = LotesEnMemoria([])

    def con_usuarios(self, usuarios: Usuarios):
        self.__usuarios = usuarios
        return self

    def con_subastas(self, subastas: Subastas):
        self.__subastas = subastas
        return self

    def con_articulos(self, articulos: Articulos):
        self.__articulos = articulos
        return self

    def con_lotes(self, lotes: Lotes):
        self.__lotes = lotes
        return self

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos, self.__lotes)
