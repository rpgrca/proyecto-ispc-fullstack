from typing import Any


class Servicio:
    def _throw_if_invalid(self, atributo: Any, mensaje: str) -> None:
        if not atributo:
            raise ValueError(mensaje)

    def _throw_if_true(self, condition: bool, mensaje: str) -> None:
        if condition:
            raise ValueError(mensaje)

    def _throw(self, mensaje: str) -> None:
        raise ValueError(mensaje)

    def _throw_if_not_positive(self, uid: int, mensaje: str) -> None:
        if type(uid) is not int or uid <= 0:
            raise ValueError(mensaje)
