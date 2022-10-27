import unittest
from ddt import ddt, data, unpack
import tests.constantes as C
from controller.login import LoginController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class LoginControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({
                C.NOMBRE_USUARIO: {
                    "id": C.ID_USUARIO,
                    "nombre": C.NOMBRE_USUARIO,
                    "apellido": C.APELLIDO_USUARIO,
                    "email": C.EMAIL_USUARIO,
                    "usuario": C.NOMBRE_USUARIO,
                    "clave": C.CLAVE_USUARIO,
                    "nacimiento": C.FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Pujador.value
                }})) \
            .construir()

    def test_retornar_ok_cuando_usuario_y_clave_son_correctos(self):
        sut = LoginController(self.__db_con_usuario, C.NOMBRE_USUARIO, C.CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(C.NOMBRE_USUARIO, respuesta["mensaje"])

    @data(
        (C.NOMBRE_USUARIO, C.OTRA_CLAVE_USUARIO),
        (C.OTRO_NOMBRE_USUARIO, C.CLAVE_USUARIO)
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

        sut = LoginController(db, C.NOMBRE_USUARIO, C.CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoginController.LOGIN_INVALIDO, respuesta["mensaje"])

    @data(
        ("", C.CLAVE_USUARIO, LoginController.SIN_USUARIO),
        (None, C.CLAVE_USUARIO, LoginController.SIN_USUARIO),
        (C.NOMBRE_USUARIO, "", LoginController.SIN_CLAVE),
        (C.NOMBRE_USUARIO, None, LoginController.SIN_CLAVE)
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
