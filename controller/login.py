# login.py
#
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class LoginController:
    def __init__(self, usuario: str, clave: str):
        model
        self.__usuario = usuario
        self.__clave = clave
        self.__response = { "status": "error" }

        if usuario in Login.__usuarios:
            if Login.__usuarios[usuario] == clave:
                self.__response = { "status": "ok" }

    def obtener_respuesta(self):
        return self.__response
