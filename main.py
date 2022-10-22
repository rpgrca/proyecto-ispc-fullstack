import uvicorn
from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from model.usuarios import UsuariosImplementadoConDiccionario
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

db = UsuariosImplementadoConDiccionario({
    "Roberto": { "clave": "123456", "email": "roberto.carlos.alfonso@gmail.com" },
    "Martin": { "clave": "654321", "email": "martin@gmail.com" },
    "Julia": { "clave": "109283", "email": "julia@gmail.com" },
    "Estela": { "clave": "777777", "email": "estela@gmail.com" }
})

@app.post("/ingresar/", status_code=200)
def ingresar(usuario: str = Form(), clave: str = Form(), response: Response = Response()):
    respuesta = LoginController(db, usuario, clave).obtener_respuesta()
    if respuesta["status"] != "ok":
        response.status_code = 401

    return respuesta

@app.post("/registrar/", status_code=200)
def registrar(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(), clave: str = Form(), nacimiento: str = Form(), response: Response = Response()):
    respuesta = RegistroController(db, nombre, apellido, email, usuario, clave, nacimiento).obtener_respuesta()
    if respuesta["status"] != "ok":
        response.status_code = 401

    return respuesta

@app.post("/reestablecer/", status_code=200)
def reestablecer(email: str = Form(), response: Response = Response()):
    respuesta = ReestablecerController(db, email).obtener_respuesta()
    if respuesta["status"] != "ok":
        response.status_code = 401

    return respuesta

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
