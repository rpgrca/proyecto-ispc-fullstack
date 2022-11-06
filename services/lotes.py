from .servicio import Servicio
from model.database import BaseDeDatos
from model.lotes import Lote


class ServicioLote(Servicio):
    LOTE_SIN_SUBASTA = "No se puede agregar un lote sin subasta"
    ARTICULO_NULO_EN_SUBASTA = "No se puede agregar un articulo nulo a una subasta"
    LOTE_SUBASTA_INEXISTENTE = "No se puede agregar un lote a una subasta inexistente"
    ARTICULO_INEXISTENTE = "No se puede agregar un articulo inexistente a una subasta"
    BUSCAR_SIN_SUBASTA = "No se puede buscar un lote sin subasta"
    CONTAR_SUBASTA_INEXISTENTE = "No se puede contar lotes de una subasta inexistente"
    CONTAR_SIN_SUBASTA = "No se puede contar lotes sin subasta"
    SUBASTA_INEXISTENTE = "No se puede subastar un lote de una subasta inexistente"
    LOTE_INEXISTENTE = "No existe tal lote"
    BASE_INVALIDA = "No se puede agregar un artículo con base inválida"
    ORDEN_INVALIDO = "No se puede agregar un artículo con orden inválido"
    LISTAR_SIN_SUBASTA = "No se puede listar lotes de una subasta inválida"
    LISTAR_CON_SUBASTA_INEXISTENTE = "No se puede listar lotes de una subasta inexistente"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, subasta_uid: int, articulo_uid: str, base: int, orden: int) -> None:
        self._throw_if_not_positive(subasta_uid, self.LOTE_SIN_SUBASTA)
        self._throw_if_not_positive(articulo_uid, self.ARTICULO_NULO_EN_SUBASTA)
        self._throw_if_not_positive(base, self.BASE_INVALIDA)
        self._throw_if_invalid(orden, self.ORDEN_INVALIDO)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.LOTE_SUBASTA_INEXISTENTE)

        articulo = self.__db.Articulos.buscar_por_uid(articulo_uid)
        self._throw_if_invalid(articulo, self.ARTICULO_INEXISTENTE)

        self.__db.Lotes.agregar(subasta, articulo, base, orden)

    def contar_lotes_en(self, subasta_uid: int) -> int:
        self._throw_if_not_positive(subasta_uid, self.CONTAR_SIN_SUBASTA)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.CONTAR_SUBASTA_INEXISTENTE)

        return self.__db.Lotes.contar_lotes(subasta)

    def obtener(self, subasta_uid: int, orden: int) -> Lote:
        self._throw_if_not_positive(subasta_uid, self.BUSCAR_SIN_SUBASTA)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.SUBASTA_INEXISTENTE)

        if orden < 1:
            self._throw(self.LOTE_INEXISTENTE)

        lote = self.__db.Lotes.obtener(subasta, orden)
        if not lote:
            self._throw(self.LOTE_INEXISTENTE)

        return lote

    def listar(self, subasta_uid: int) -> list[Lote]:
        self._throw_if_not_positive(subasta_uid, self.LISTAR_SIN_SUBASTA)

        subasta = self.__db.Subastas.buscar_por_uid(subasta_uid)
        self._throw_if_invalid(subasta, self.LISTAR_CON_SUBASTA_INEXISTENTE)

        return self.__db.Lotes.listar(subasta)
