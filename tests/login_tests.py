import unittest
from ddt import ddt, data, unpack
from controller.login import LoginController
from model.tipo_usuario import TipoDeUsuario
from model.base_temporal import UsuariosFake, CreadorDeBasesDeDatosTemporales

@ddt
class LoginControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake({
                "Roberto": {
                    "nombre": "Roberto",
                    "apellido": "Perez",
                    "email": "roberto@gmail.com",
                    "usuario": "Roberto",
                    "clave": "123456",
                    "nacimiento": 9/17/2000,
                    "tipo": TipoDeUsuario.Pujador.value
                }})) \
            .construir()

    def test_retornar_ok_cuando_usuario_y_clave_son_correctos(self):
        sut = LoginController(self.__db_con_usuario, "Roberto", "123456")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Roberto", respuesta["mensaje"])

    @data(
        ("Roberto", "123"),
        ("Carlos", "123456")
    )
    @unpack
    def test_retornar_error_cuando_usuario_o_clave_incorrecta(self, usuario: str, clave: str):
        sut = LoginController(self.__db_con_usuario, usuario, clave)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoginController.LOGIN_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_cuando_base_esta_vacia(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake({})) \
            .construir()

        sut = LoginController(db, "Roberto", "123456")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoginController.LOGIN_INVALIDO, respuesta["mensaje"])

    @data(
        ("", "123456", LoginController.SIN_USUARIO),
        (None, "123456", LoginController.SIN_USUARIO),
        ("Roberto", "", LoginController.SIN_CLAVE),
        ("Roberto", None, LoginController.SIN_CLAVE)
    )
    @unpack
    def test_retornar_error_cuando_falta_dato(self, usuario: str, clave: str, mensaje_error: str):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake({})) \
            .construir()
        sut = LoginController(db, usuario, clave)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()