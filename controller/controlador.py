from model.serialization import Serializable


class Controlador:
    def __init__(self):
        self.__respuesta = {}

    def _responder_bien_con(self, mensaje: str) -> None:
        self.__respuesta = {"status": "ok", "mensaje": mensaje}

    def _responder_bien_incluyendo_id(self, mensaje: str, id: int) -> None:
        self.__respuesta = {"status": "ok", "mensaje": mensaje, "id": id}

    def _responder_bien_serializando_item(self, model: Serializable) -> None:
        self.__respuesta = {"status": "ok", "item": model.serialize()}

    def _responder_bien_serializando_lista(self, models: list[Serializable]) -> None:
        self.__respuesta = {"status": "ok", "items": [m.serialize() for m in models]}

    def _responder_bien_con_numero(self, key: str, valor: int) -> None:
        self.__respuesta = {"status": "ok", key: valor}

    def _responder_mal_con(self, mensaje: str) -> None:
        self.__respuesta = {"status": "error", "mensaje": mensaje}

    def obtener_respuesta(self) -> dict[str, str]:
        return self.__respuesta
