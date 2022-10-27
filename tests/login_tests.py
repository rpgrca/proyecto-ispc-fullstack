import unittest
from ddt import ddt, data, unpack
from tests.constantes import *
from controller.login import LoginController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class LoginControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({
                NOMBRE_USUARIO: {
                    "id": ID_USUARIO,
                    "nombre": NOMBRE_USUARIO,
                    "apellido": APELLIDO_USUARIO,
                    "email": EMAIL_USUARIO,
                    "usuario": NOMBRE_USUARIO,
                    "clave": CLAVE_USUARIO,
                    "nacimiento": FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Pujador.value
                }})) \
            .construir()

    def test_retornar_ok_cuando_usuario_y_clave_son_correctos(self):
        sut = LoginController(self.__db_con_usuario, NOMBRE_USUARIO, CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(NOMBRE_USUARIO, respuesta["mensaje"])

    @data(
        (NOMBRE_USUARIO, OTRA_CLAVE_USUARIO),
        (OTRO_NOMBRE_USUARIO, CLAVE_USUARIO)
    )
    @unpack
    def test_retornar_error_cuando_usuario_o_clave_incorrecta(self, usuario: str, clave: str):
        sut = LoginController(self.__db_con_usuario, usuario, clave)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoginController.LOGIN_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_cuando_base_esta_vacia(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        sut = LoginController(db, NOMBRE_USUARIO, CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoginController.LOGIN_INVALIDO, respuesta["mensaje"])

    @data(
        ("", CLAVE_USUARIO, LoginController.SIN_USUARIO),
        (None, CLAVE_USUARIO, LoginController.SIN_USUARIO),
        (NOMBRE_USUARIO, "", LoginController.SIN_CLAVE),
        (NOMBRE_USUARIO, None, LoginController.SIN_CLAVE)
    )
    @unpack
    def test_retornar_error_cuando_falta_dato(self, usuario: str, clave: str, mensaje_error: str):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()
        sut = LoginController(db, usuario, clave)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()

