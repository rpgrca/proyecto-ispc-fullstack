import uuid

class Controller:
    def __init__(self):
        self.__respuesta = {}

    def _verificar(self, atributo: str, mensaje_de_error: str) -> bool:
        if not atributo:
            self.__respuesta = { "status": "error", "mensaje": mensaje_de_error }
            return False

        return True

    def _responder_bien_con(self, mensaje: str) -> None:
        self.__respuesta = { "status": "ok", "mensaje": mensaje }

    def _responder_bien_incluyendo_id(self, mensaje: str, id: uuid) -> None:
        self.__respuesta = { "status": "ok", "mensaje": mensaje, "id": str(id) }

    def _responder_mal_con(self, mensaje: str) -> None:
        self.__respuesta = { "status": "error", "mensaje": mensaje }

    def obtener_respuesta(self) -> dict[str, str]:
        return self.__respuesta