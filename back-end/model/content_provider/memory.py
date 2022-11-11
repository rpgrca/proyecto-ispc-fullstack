from datetime import date
from model.tipo_usuario import TipoDeUsuario
from model.database import BaseDeDatos
from model.articulos import Articulo
from model.usuarios import Consignatario, Martillero, Pujador, Usuarios, Usuario
from model.subastas import Subastas, Subasta
from model.articulos import Articulos
from model.pujas import Puja, Pujas
from model.lotes import Lote, Lotes
from model.libro_diario import Venta, LibroDiario


class UsuariosEnMemoria(Usuarios):
    def __init__(self, usuarios: dict):
        self.__usuarios = usuarios
        self.__id = len(self.__usuarios) + 1

    def __getitem__(self, key):
        return self.__usuarios[key]

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
            "tipo": tipo
        }
        self.__id += 1

    def existe(self, usuario: str) -> bool:
        return usuario in self.__usuarios

    def buscar(self, usuario: str, clave: str) -> Usuario:
        if usuario in self.__usuarios:
            registro = self.__usuarios[usuario]
            if registro["clave"] == clave:
                return Usuarios.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                      registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_por_email(self, email: str) -> Usuario:
        registro = next(filter(lambda u: u["email"] == email, self.__usuarios.values()), None)
        if registro:
            return Usuarios.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                  registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_pujador_por_uid(self, uid: int) -> Pujador:
        return self._buscar_por_uid_y_tipo(uid, TipoDeUsuario.Pujador)

    def buscar_consignatario_por_uid(self, uid: int) -> Consignatario:
        return self._buscar_por_uid_y_tipo(uid, TipoDeUsuario.Consignatario)

    def _buscar_por_uid_y_tipo(self, uid: int, tipo: TipoDeUsuario) -> Usuario:
        registro = next(filter(lambda u: u["id"] == uid and u["tipo"] == tipo, self.__usuarios.values()), None)
        if registro:
            return Usuarios.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                  registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def buscar_usuario_por_uid(self, uid: int) -> Usuario:
        registro = next(filter(lambda u: u["id"] == uid, self.__usuarios.values()), None)
        if registro:
            return Usuarios.crear(registro["id"], registro["nombre"], registro["apellido"], registro["email"],
                                  registro["usuario"], registro["clave"], registro["nacimiento"], registro["tipo"])

        return None

    def actualizar(self, cuenta: Usuario, usuario: str, email: str, clave: str) -> None:
        del self.__usuarios[cuenta.obtener_usuario()]
        self.__usuarios[usuario] = {
            "id": cuenta.obtener_uid(),
            "nombre": cuenta.obtener_nombre(),
            "apellido": cuenta.obtener_apellido(),
            "usuario": usuario,
            "clave": clave,
            "email": email,
            "nacimiento": cuenta.obtener_nacimiento(),
            "tipo": cuenta.obtener_tipo()
        }

    def buscar_martillero(self) -> Martillero:
        return next(filter(lambda u: u["tipo"] == TipoDeUsuario.Martillero, self.__usuarios.values()), None)


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

    def crear(self, titulo: str, descripcion: str, valuacion: int, consignatario: Consignatario) -> Articulo:
        articulo = Articulo(len(self.__articulos) + 1, titulo, descripcion, valuacion, consignatario)
        self.__articulos.append(articulo)
        return articulo

    def buscar_por_uid(self, uid: int) -> Articulo:
        return next(filter(lambda s: s.obtener_uid() == uid, self.__articulos), None)

    def listar_articulos_propiedad_de(self, consignatario: Consignatario) -> list[Articulo]:
        return [art for art in self.__articulos if art.obtener_consignatario_uid() == consignatario.obtener_uid()]

    def contar(self) -> int:
        return len(self.__articulos)

    def listar(self) -> list[Articulo]:
        return self.__articulos

    def borrar(self, uid: int) -> None:
        self.__articulos = [articulo for articulo in self.__articulos if articulo.obtener_uid() != uid]

    def actualizar(self, articulo: Articulo, titulo: str, descripcion: str, valuacion: str,
                   consignatario: Consignatario) -> None:
        articulos = []
        for actual in self.__articulos:
            if actual.obtener_uid() != articulo.obtener_uid():
                articulos.append(actual)
            else:
                articulos.append(Articulo(actual.obtener_uid(), titulo, descripcion, valuacion, consignatario))

        self.__articulos = articulos


class PujasEnMemoria(Pujas):
    def __init__(self, pujas: list[Puja]):
        self.__pujas = pujas
        self.__next_id = len(self.__pujas) + 1

    def agregar(self, monto: int, pujador: Pujador, lote: Lote):
        self.__pujas.append(Puja(self.__next_id, monto, pujador, lote))
        self.__next_id += 1

    def buscar_ultima_puja(self, lote: Lote) -> Puja:
        return next(filter(lambda p: p.obtener_lote().obtener_uid() == lote.obtener_uid(), reversed(self.__pujas)), None)

    def buscar_por_uid(self, uid: int) -> Puja:
        return next(filter(lambda p: p.obtener_uid() == uid, self.__pujas), None)

    def buscar_por_lote(self, lote: Lote) -> list[Puja]:
        return [puja for puja in self.__pujas if puja.obtener_lote().obtener_uid() == lote.obtener_uid()]


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

    def listar(self, subasta: Subasta) -> list[Lote]:
        return sorted([lote for lote in self.__lotes if lote.obtener_subasta_uid() == subasta.obtener_uid()],
                      key=lambda x: x.obtener_orden())

    def existe_con_articulo(self, articulo: Articulo) -> bool:
        return any(lote.obtener_articulo_uid() == articulo.obtener_uid() for lote in self.__lotes) > 0


class LibroDiarioEnMemoria(LibroDiario):
    def __init__(self, ventas: list[Venta]):
        self.__ventas = ventas

    def crear(self, puja: Puja, precio_final: float, comision: float, pago_a_consignatario: float) -> Venta:
        venta = Venta(len(self.__ventas) + 1, puja, precio_final, comision, pago_a_consignatario)
        self.__ventas.append(venta)
        return venta

    def buscar_por_uid(self, uid: int) -> Venta:
        return next(filter(lambda v: v.obtener_uid() == uid, self.__ventas), None)

    def listar_compras_de(self, pujador: Pujador):
        return [venta for venta in self.__ventas if venta.obtener_ganador().obtener_uid() == pujador.obtener_uid()]


class CreadorDeBasesDeDatosTemporales:
    def __init__(self):
        self.__usuarios = UsuariosEnMemoria({})
        self.__subastas = SubastasEnMemoria([])
        self.__articulos = ArticulosEnMemoria([])
        self.__lotes = LotesEnMemoria([])
        self.__pujas = PujasEnMemoria([])
        self.__ventas = LibroDiarioEnMemoria([])

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

    def con_ventas(self, ventas: LibroDiario):
        self.__ventas = ventas
        return self

    def construir(self) -> BaseDeDatos:
        return BaseDeDatos(self.__usuarios, self.__subastas, self.__articulos, self.__lotes, self.__pujas, self.__ventas)
