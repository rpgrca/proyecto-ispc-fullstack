import unittest
from ddt import ddt, data, unpack
import tests.constantes as C
from controller.articulo import ControladorArticulo
from services.articulos import ServicioArticulos
from model.articulos import Articulo
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria, UsuariosEnMemoria
from model.tipo_usuario import TipoDeUsuario


@ddt
class ControladorArticuloTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({
                C.NOMBRE_USUARIO: {
                    "id": 1,
                    "nombre": C.NOMBRE_USUARIO,
                    "apellido": C.APELLIDO_USUARIO,
                    "email": C.EMAIL_USUARIO,
                    "usuario": C.NOMBRE_USUARIO,
                    "clave": C.CLAVE_USUARIO,
                    "tipo": TipoDeUsuario.Consignatario
                }})) \
            .con_subastas(SubastasEnMemoria([])) \
            .con_articulos(ArticulosEnMemoria([Articulo(C.ARTICULO_UID)])) \
            .construir()

    @data("", None)
    def test_retornar_error_creando_articulo_con_titulo_invalido(self, titulo_invalido):
        sut = ControladorArticulo(self.__db)
        sut.agregar(titulo_invalido, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.TITULO_INVALIDO, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()
