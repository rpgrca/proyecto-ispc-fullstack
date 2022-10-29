from datetime import date
from model.articulos import Articulo
from model.database import BaseDeDatos
from model.usuarios import Consignatario, Pujador, Usuarios, Usuario, UsuariosFactory
from model.subastas import Subastas, Subasta
from model.articulos import Articulos
from model.pujas import Puja, Pujas
from model.tipo_usuario import TipoDeUsuario
from model.lotes import Lote, Lotes


class UsuariosEnMemoria(Usuarios):
    def __init__(self, usuarios: dict):
        self.__usuarios = usuarios
        self.__id = len(self.__usuarios) + 1

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

    def buscar(self, usuario: str, clave: str) -> Usuario:
        if usuario in self.__usuarios:
            registro = self.__usuarios[usuario]
            if registro["clave"] == clave:
                return UsuariosFactory.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                             registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_por_email(self, email: str) -> Usuario:
        registro = next(filter(lambda u: u["email"] == email, self.__usuarios.values()), None)
        if registro:
            return UsuariosFactory.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                         registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_pujador_por_uid(self, uid: int) -> Pujador:
        registro = next(filter(lambda u: u["id"] == uid and u["tipo"] == TipoDeUsuario.Pujador.value,
                               self.__usuarios.values()), None)
        if registro:
            return UsuariosFactory.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                         registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None


class SubastasEnMemoria(Subastas):
    def __init__(self, subastas: list[Subasta]):
        self.__subastas = subastas

    def crear(self, titulo: str, descripcion: str, imagen: str, fecha: date) -> Subasta:
        subasta = Subasta(len(self.__subastas) + 1, titulo, descripcion, imagen, fecha)
        self.__subastas.append(subasta)
        return subasta

    def buscar_por_uid(self, uid: int) -> Subasta:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__subastas), None)


class ArticulosEnMemoria(Articulos):
    def __init__(self, articulos: list[Articulo]):
        self.__articulos = articulos

    def agregar(self, uid: int) -> None:
        self.__articulos.append(Articulo(uid))

    def buscar_por_uid(self, uid: int) -> Articulo:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__articulos), None)

    def listar_articulos_propiedad_de(self, consignatario: Consignatario) -> list[Articulo]:
        return [art for art in self.__articulos if art.obtener_consignatario_uid() == consignatario.obtener_uid()]


class PujasEnMemoria(Pujas):
    def __init__(self, pujas: list[Puja]):
        self.__pujas = pujas
        self.__next_id = len(self.__pujas) + 1

    def agregar(self, monto: int, pujador: Pujador, lote: Lote):
        self.__pujas.append(Puja(self.__next_id, monto, pujador, lote))
        self.__next_id += 1

    def buscar_por_monto(self, monto: int) -> Puja:
        pass

    def buscar_ultima_puja(self, lote: Lote) -> Puja:
        return next(filter(lambda p: p.obtener_lote_uid() == lote.obtener_uid(), reversed(self.__pujas)), None)

    def buscar_por_uid(self, uid: int) -> Puja:
        return next(filter(lambda p: p.obtener_uid() == uid, self.__pujas), None)

    def buscar_por_lote(self, lote: Lote) -> list[Puja]:
        return [puja for puja in self.__pujas if puja.obtener_lote_uid() == lote.obtener_uid()]


class LotesEnMemoria(Lotes):
    def __init__(self, lotes: list[Lote]):
        self.__lotes = lotes

    def agregar(self, subasta: Subasta, articulo: Articulo, base: int, orden: int):
        self.__lotes.append(Lote(len(self.__lotes) + 1, subasta, articulo, base, orden))

    def contar_lotes(self, subasta: Subasta) -> int:
        return sum(1 if lote.obtener_subasta_uid() == subasta.obtener_uid() else 0 for lote in self.__lotes)

    def obtener(self, subasta: Subasta, orden: int) -> Lote:
        return next((lote for lote in self.__lotes if lote.obtener_subasta_uid() == subasta.obtener_uid() and
                    lote.obtener_orden() == orden), None)

    def buscar_por_uid(self, lote_uid: int) -> Lote:
        return next(filter(lambda l: l.obtener_uid() == lote_uid, self.__lotes), None)


class CreadorDeBasesDeDatosTemporales:
    def __init__(self):
        self.__usuarios = UsuariosEnMemoria({
            "Roberto": {
                "id": 1,
                "nombre": "Roberto",
                "apellido": "Perez",
                "usuario": "Roberto",
                "clave": "123456",
                "email": "roberto.carlos.alfonso@gmail.com",
                "nacimiento": 17/9/2000,
                "tipo": TipoDeUsuario.Pujador
            },
            "Martin": {
                "id": 2,
                "nombre": "Martin",
                "apellido": "Rodriguez",
                "usuario": "Martin",
                "clave": "654321",
                "email": "martin@gmail.com",
                "nacimiento": 10/5/2000,
                "tipo": TipoDeUsuario.Pujador
            },
            "Julia": {
                "id": 3,
                "nombre": "Julia",
                "apellido": "Gonzalez",
                "usuario": "Julia",
                "clave": "109283",
                "email": "julia@gmail.com",
                "nacimiento": 12/12/2000,
                "tipo": TipoDeUsuario.Pujador
            },
            "Estela": {
                "id": 4,
                "nombre": "Estela",
                "apellido": "Flores",
                "usuario": "Estela",
                "clave": "777777",
                "email": "estela@gmail.com",
                "nacimiento": 6/6/2000,
                "tipo": TipoDeUsuario.Consignatario
            },
            "Adrian": {
                "id": 5,
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
        self.__pujas = PujasEnMemoria([])

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

    def con_pujas(self, pujas: Pujas):
        self.__pujas = pujas
        return self

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos, self.__lotes, self.__pujas)
