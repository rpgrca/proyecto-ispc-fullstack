from fastapi import FastAPI, Form
from controller.login import LoginController

app = FastAPI()

@app.post("/ingresar/")
def ingresar(usuario: str = Form(), clave: str = Form()):
    return LoginController(usuario, clave).obtener_respuesta()
