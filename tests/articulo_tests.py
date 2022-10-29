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
                    "nacimiento": C.FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Consignatario.value
                }})) \
            .con_subastas(SubastasEnMemoria([])) \
            .con_articulos(ArticulosEnMemoria([])) \
            .construir()

    @data("", None)
    def test_retornar_error_creando_articulo_con_titulo_invalido(self, titulo_invalido):
        sut = ControladorArticulo(self.__db)
        sut.agregar(titulo_invalido, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.TITULO_INVALIDO, respuesta["mensaje"])

    @data("", None)
    def test_retornar_error_creando_articulo_con_descripcion_invalida(self, descripcion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, descripcion_invalida, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.DESCRIPCION_INVALIDA, respuesta["mensaje"])

    @data(-1, 0)
    def test_retornar_error_creando_articulo_con_valuacion_invalida(self, valuacion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, valuacion_invalida, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.VALUACION_INVALIDA, respuesta["mensaje"])

    @data(-1, 0)
    def test_retornar_error_creando_articulo_con_consignatario_invalido(self, consignatario_invalido):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, consignatario_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.CONSIGNATARIO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_creando_articulo_con_consignatario_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.CONSIGNATARIO_INEXISTENTE, respuesta["mensaje"])

    def test_crear_articulo_correctamente(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorArticulo.ARTICULO_CREADO, respuesta["mensaje"])

    def test_crear_articulo_con_datos_correctos(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        articulo = self.__db.Articulos.buscar_por_uid(1)
        self.assertEqual(1, articulo.obtener_uid())
        # TODO: cuando se complete articulo
        #self.assertEqual(C.TITULO_ARTICULO, articulo.obtener_titulo())
        #self.assertEqual(C.DESCRIPCION_ARTICULO, articulo.obtener_descripcion())
        #self.assertEqual(C.VALUACION_ARTICULO, articulo.obtener_valuacion())
        #self.assertEqual(1, articulo.obtener_consignatario_uid())


if __name__ == "__main__":
    unittest.main()
