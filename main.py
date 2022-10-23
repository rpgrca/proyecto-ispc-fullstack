import uvicorn
from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from model.transcient_database import CreadorDeBasesDeDatosTemporales
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

db = CreadorDeBasesDeDatosTemporales().construir()

def __cambiar_status_code(respuesta: dict[str, str], response: Response):
    if respuesta["status"] != "ok":
        response.status_code = 401


@app.post("/ingresar/", status_code=200)
def ingresar(usuario: str = Form(), clave: str = Form(), response: Response = Response()):
    controlador = LoginController(db, usuario, clave)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/registrar/", status_code=200)
def registrar(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(), clave: str = Form(), nacimiento: str = Form(), response: Response = Response()):
    controlador = RegistroController(db, nombre, apellido, email, usuario, clave, nacimiento)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/reestablecer/", status_code=200)
def reestablecer(email: str = Form(), response: Response = Response()):
    controlador = ReestablecerController(db, email)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")