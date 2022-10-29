from controller.controlador import Controlador
from controller.servicio import Servicio
from model.database import BaseDeDatos


class ControladorPuja(Controlador):
    PUJA_REALIZADA = "Puja realizada con éxito"

    def __init__(self, db: BaseDeDatos):
        self.__db = db

    def agregar(self, lote_uid: int, pujador_uid: int, monto: int) -> None:
        try:
            ServicioPuja(self.__db).agregar(lote_uid, pujador_uid, monto)
            self._responder_bien_con(self.PUJA_REALIZADA)
        except Exception as err:
            self._responder_mal_con(str(err))
            
    def listar(self, lote_uid: int) -> None:
        try:
            pujas = ServicioPuja(self.__db).listar(lote_uid)
            self._responder_bien_serializando_lista(pujas)
        except Exception as err:
            self._responder_mal_con(str(err))


class ServicioPuja(Servicio):
    PUJAR_SIN_LOTE = "No se puede pujar sin lote"
    PUJAR_SIN_PUJADOR = "No se puede pujar sin un pujador"
    PUJAR_SIN_PUJA = "No se puede pujar sin un monto"
    LOTE_INEXISTENTE = "No se puede pujar por un lote inexistente"
    PUJADOR_INEXISTENTE = "No se puede pujar con un pujador inexistente"
    PUJA_BAJA = "No se puede pujar por menos de la última puja"
    MONTO_INVALIDO = "No se puede pujar por montos menores o iguales a cero"

    def __init__(self, db: BaseDeDatos):
        super().__init__()
        self.__db = db

    def agregar(self, lote_uid: int, pujador_uid: int, monto: int) -> None:
        self._throw_if_invalid(lote_uid, self.PUJAR_SIN_LOTE)
        self._throw_if_invalid(pujador_uid, self.PUJAR_SIN_PUJADOR)
        self._throw_if_invalid(monto, self.PUJAR_SIN_PUJA)

        lote = self.__db.Lotes.buscar_por_uid(lote_uid)
        self._throw_if_invalid(lote, self.LOTE_INEXISTENTE)

        pujador = self.__db.Usuarios.buscar_pujador_por_uid(pujador_uid)
        self._throw_if_invalid(pujador, self.PUJADOR_INEXISTENTE)

        if monto <= 0:
            self._throw(self.MONTO_INVALIDO)

        puja = self.__db.Pujas.buscar_ultima_puja(lote)
        if puja and puja.obtener_monto() >= monto:
            self._throw(self.PUJA_BAJA)

        self.__db.Pujas.agregar(monto, pujador, lote)

    def listar(self, lote_uid: int) -> None:
        self._throw_if_invalid(lote_uid, self.PUJAR_SIN_LOTE)

        lote = self.__db.Lotes.buscar_por_uid(lote_uid)
        self._throw_if_invalid(lote, self.LOTE_INEXISTENTE)

        return self.__db.Pujas.buscar_por_lote(lote)
