from fastapi import FastAPI, Form, Response, status
from fastapi.middleware.cors import CORSMiddleware
from controller.login import LoginController
from controller.registro import RegistroController
from controller.reestablecer import ReestablecerController

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/ingresar/", status_code=200)
def ingresar(usuario: str = Form(), clave: str = Form(), response: Response = Response()):
    respuesta = LoginController(usuario, clave).obtener_respuesta()
    if respuesta["status"] != "ok":
        response.status_code = 401

    return respuesta

@app.post("/registrar/", status_code=200)
def registrar(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(), clave: str = Form(), nacimiento: str = Form(), response: Response = Response()):
    respuesta = RegistroController(nombre, apellido, email, usuario, clave, nacimiento).obtener_respuesta()
    if respuesta["status"] != "ok":
        response.status_code = 401

    return respuesta

@app.post("/reestablecer/", status_code=200)
def reestablecer(email: str = Form(), response: Response = Response()):
    respuesta = ReestablecerController(email).obtener_respuesta()
    if respuesta["status"] != "ok":
        response.status_code = 401

    return respuesta
