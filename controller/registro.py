# registro.py
#
# registrar(usuario, email, password)
from fastapi import FastAPI
from model.usuarios import Usuarios

class RegistroController:
    def __init__(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        if Usuarios().existe(usuario):
            self.__resultado = { "status": "error", "mensaje": "La cuenta ya existe" }
        else:
            self.__resultado = { "status": "ok", "mensaje": "La cuenta ha sido creada correctamente" }

    def obtener_respuesta(self):
        return self.__resultado
