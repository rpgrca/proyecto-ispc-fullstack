from fastapi import FastAPI, Form
from controller.login import LoginController
from controller.registro import RegistroController
from controller.reestablecer import ReestablecerController

app = FastAPI()

@app.post("/ingresar/")
def ingresar(usuario: str = Form(), clave: str = Form()):
    return LoginController(usuario, clave).obtener_respuesta()

@app.post("/registrar/")
def registrar(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(), clave: str = Form(), nacimiento: str = Form()):
    return RegistroController(nombre, apellido, email, usuario, clave, nacimiento).obtener_respuesta()

@app.post("/reestablecer/")
def reestablecer(email: str = Form()):
    return ReestablecerController(email).obtener_respuesta()

