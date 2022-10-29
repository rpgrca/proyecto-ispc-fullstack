import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.articulo import ControladorArticulo
from services.articulos import ServicioArticulos
from model.content_provider.memory import CreadorDeBasesDeDatosTemporales
from model.content_provider.memory import ArticulosEnMemoria, SubastasEnMemoria, UsuariosEnMemoria
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

    @data("", None, -1, 0)
    def test_retornar_error_creando_articulo_con_valuacion_invalida(self, valuacion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, valuacion_invalida, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.VALUACION_INVALIDA, respuesta["mensaje"])

    @data("", None, -1, 0)
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

    def test_retornar_ok_al_crear_correctamente(self):
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

    def test_retornar_articulo_al_buscar_articulo_creado(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.buscar_por_uid(1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual({"consignatario_id": 1, "id": 1}, respuesta["item"])

    @data(None, "", -1, 0)
    def test_retornar_error_al_buscar_articulo_invalido(self, uid_invalido):
        sut = ControladorArticulo(self.__db)
        sut.buscar_por_uid(uid_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.UID_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_al_buscar_articulo_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.buscar_por_uid(C.OTRO_ARTICULO_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_articulos_al_buscar_por_consignatario_existente_con_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.agregar(C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        sut.listar_articulos_propiedad_de(1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, len(respuesta["items"]))
        self.assertIn({"consignatario_id": 1, "id": 1}, respuesta["items"])
        self.assertIn({"consignatario_id": 1, "id": 2}, respuesta["items"])

    def test_retonar_vacio_al_buscar_por_consignatario_existente_sin_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.listar_articulos_propiedad_de(1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([], respuesta["items"])

    @data(None, "", -1, 0)
    def test_retornar_error_al_buscar_por_consignatario_invalido(self, uid_invalido):
        sut = ControladorArticulo(self.__db)
        sut.listar_articulos_propiedad_de(uid_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.LISTAR_CON_CONSIGNATARIO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_al_buscar_por_consignatario_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.listar_articulos_propiedad_de(C.OTRO_ID_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.LISTAR_CON_CONSIGNATARIO_INEXISTENTE, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()
