from datetime import date
import uvicorn
from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from controller.subasta import SubastaController
from model.base_temporal import CreadorDeBasesDeDatosTemporales
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


def __cambiar_status_code(respuesta: dict[str, str], response: Response, status_code=status.HTTP_401_UNAUTHORIZED):
    if respuesta["status"] != "ok":
        response.status_code = status_code

    return respuesta


@app.post("/ingresar/", status_code=status.HTTP_200_OK)
def ingresar(usuario: str = Form(), clave: str = Form(), response: Response = Response()):
    controlador = LoginController(db, usuario, clave)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/registrar/", status_code=status.HTTP_200_OK)
def registrar(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(), clave: str = Form(), \
    nacimiento: date = Form(), response: Response = Response()):
    controlador = RegistroController(db, nombre, apellido, email, usuario, clave, nacimiento)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/reestablecer/", status_code=status.HTTP_200_OK)
def reestablecer(email: str = Form(), response: Response = Response()):
    controlador = ReestablecerController(db, email)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/crear_subasta/", status_code=status.HTTP_200_OK)
def crear_subasta(titulo: str = Form(), descripcion: str = Form(), imagen: str = Form(), fecha: date = Form(), \
    response: Response = Response()):
    controlador = SubastaController(db)
    controlador.crear(titulo, descripcion, imagen, fecha)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/agregar_lote", status_code=status.HTTP_200_OK)
def agregar_lote(subasta_uid: str = Form(), articulo_uid: str = Form(), base: int = Form(), response: Response = Response()):
    controlador = SubastaController(db)
    controlador.agregar_lote(subasta_uid, articulo_uid, base)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/obtener_lote/{subasta_uid}/{orden}", status_code=status.HTTP_200_OK)
def obtener_lote(subasta_uid: str, orden: int, response: Response = Response()):
    controlador = SubastaController(db)
    controlador.obtener_lote(subasta_uid, orden)
    return __cambiar_status_code(controlador.obtener_respuesta(), response, status.HTTP_404_NOT_FOUND)


@app.get("/contar_lotes/{subasta_uid}", status_code=status.HTTP_200_OK)
def contar_lotes(subasta_uid: str, response: Response = Response()):
    controlador = SubastaController(db)
    controlador.contar_lotes(subasta_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
