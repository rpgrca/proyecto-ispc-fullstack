import uvicorn
from datetime import date
from fastapi import FastAPI, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.mysql import CreadorDeBasesDeDatosMySql
from model.content_provider.memory import CreadorDeBasesDeDatosTemporales
from controller.articulo import ControladorArticulo
from controller.subasta import ControladorSubasta
from controller.lote import ControladorLote
from controller.login import ControladorLogin
from controller.usuario import ControladorUsuario
from controller.puja import ControladorPuja
from controller.libro_diario import ControladorLibroDiario

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# db = CreadorDeBasesDeDatosMySql(["localhost", "root", "gTp8xT2!", "bidon_subastas"]).construir()
db = CreadorDeBasesDeDatosTemporales().construir()


def __cambiar_status_code(respuesta: dict[str, str], response: Response, status_code=status.HTTP_401_UNAUTHORIZED):
    if respuesta["status"] != "ok":
        response.status_code = status_code

    return respuesta


@app.post("/ingresar/", status_code=status.HTTP_200_OK)
def ingresar(usuario: str = Form(), clave: str = Form(), response: Response = Response()):
    controlador = ControladorLogin(db)
    controlador.login(usuario, clave)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/registrar/", status_code=status.HTTP_200_OK)
def registrar(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(), clave: str = Form(),
              nacimiento: date = Form(), response: Response = Response()):
    controlador = ControladorUsuario(db)
    controlador.agregar(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Pujador)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/reestablecer/", status_code=status.HTTP_200_OK)
def reestablecer(email: str = Form(), response: Response = Response()):
    controlador = ControladorLogin(db)
    controlador.recordar(email)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/consignatarios", status_code=status.HTTP_200_OK)
def crear_consignatario(nombre: str = Form(), apellido: str = Form(), email: str = Form(), usuario: str = Form(),
                        clave: str = Form(), nacimiento: date = Form(), response: Response = Response()):
    controlador = ControladorUsuario(db)
    controlador.agregar(nombre, apellido, email, usuario, clave, nacimiento, TipoDeUsuario.Consignatario)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/articulos", status_code=status.HTTP_200_OK)
def crear_articulo(titulo: str = Form(), descripcion: str = Form(), valuacion: int = Form(), consignatario_uid: int = Form(),
                   response: Response = Response()):
    controlador = ControladorArticulo(db)
    controlador.agregar(titulo, descripcion, valuacion, consignatario_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/articulos/contar", status_code=status.HTTP_200_OK)
def contar_articulos(response: Response = Response()):
    controlador = ControladorArticulo(db)
    controlador.contar()
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/articulos/listar/{consignatario_uid}", status_code=status.HTTP_200_OK)
def listar_articulos_de(consignatario_uid: int, response: Response = Response()):
    controlador = ControladorArticulo(db)
    controlador.listar_articulos_propiedad_de(consignatario_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/articulos", status_code=status.HTTP_200_OK)
def listar_articulos(response: Response = Response()):
    controlador = ControladorArticulo(db)
    controlador.listar()
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.delete("/articulos", status_code=status.HTTP_200_OK)
def borrar_articulo(uid: int = Form(), response: Response = Response()):
    controlador = ControladorArticulo(db)
    controlador.borrar(uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.put("/articulos", status_code=status.HTTP_200_OK)
def actualizar_articulo(uid: int = Form(), titulo: str = Form(), descripcion: str = Form(), valuacion: int = Form(),
                        consignatario_uid: int = Form(), response: Response = Response()):
    controlador = ControladorArticulo(db)
    controlador.actualizar(uid, titulo, descripcion, valuacion, consignatario_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/subastas/", status_code=status.HTTP_200_OK)
def crear_subasta(titulo: str = Form(), descripcion: str = Form(), imagen: str = Form(), fecha: date = Form(),
                  response: Response = Response()):
    controlador = ControladorSubasta(db)
    controlador.crear(titulo, descripcion, imagen, fecha)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/lotes", status_code=status.HTTP_200_OK)
def agregar_lote(subasta_uid: int = Form(), articulo_uid: int = Form(), base: int = Form(), orden: int = Form(),
                 response: Response = Response()):
    controlador = ControladorLote(db)
    controlador.agregar(subasta_uid, articulo_uid, base, orden)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/lotes/{subasta_uid}", status_code=status.HTTP_200_OK)
def obtener_lotes(subasta_uid: int, response: Response = Response()):
    controlador = ControladorLote(db)
    controlador.listar(subasta_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response, status.HTTP_404_NOT_FOUND)


@app.get("/lotes/contar/{subasta_uid}", status_code=status.HTTP_200_OK)
def contar_lotes(subasta_uid: int, response: Response = Response()):
    controlador = ControladorLote(db)
    controlador.contar_lotes_en(subasta_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response, status.HTTP_404_NOT_FOUND)


@app.post("/lotes/cerrar", status_code=status.HTTP_200_OK)
def cerrar(lote_uid: int = Form(), response: Response = Response()):
    controlador = ControladorLibroDiario(db)
    controlador.registrar_venta_en(lote_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/lotes/{subasta_uid}/{orden}", status_code=status.HTTP_200_OK)
def obtener_lote(subasta_uid: int, orden: int, response: Response = Response()):
    controlador = ControladorLote(db)
    controlador.obtener(subasta_uid, orden)
    return __cambiar_status_code(controlador.obtener_respuesta(), response, status.HTTP_404_NOT_FOUND)


@app.post("/pujas", status_code=status.HTTP_200_OK)
def pujar(lote_uid: int = Form(), pujador_uid: int = Form(), monto: int = Form(), response: Response = Response()):
    controlador = ControladorPuja(db)
    controlador.agregar(lote_uid, pujador_uid, monto)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.get("/pujas/{lote_uid}", status_code=status.HTTP_200_OK)
def obtener_pujas(lote_uid: int, response: Response = Response()):
    controlador = ControladorPuja(db)
    controlador.listar(lote_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


@app.post("/vender", status_code=status.HTTP_200_OK)
def vender(puja_uid: int = Form(), response: Response = Response()):
    controlador = ControladorLibroDiario(db)
    controlador.convertir_en_venta(puja_uid)
    return __cambiar_status_code(controlador.obtener_respuesta(), response)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
