import unittest
from ddt import ddt, data, unpack
import tests.constantes as C
from controller.login import ControladorLogin, ServicioLogin
from tests.email_sender_spy import EmailSenderSpy
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class ServicioLoginTests(unittest.TestCase):
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
                    "tipo": TipoDeUsuario.Pujador
                }})) \
            .construir()

    def test_retornar_ok_cuando_usuario_y_clave_son_correctos(self):
        sut = ControladorLogin(self.__db_con_usuario)
        sut.login(C.NOMBRE_USUARIO, C.CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(C.NOMBRE_USUARIO, respuesta["mensaje"])

    @data(
        (C.NOMBRE_USUARIO, C.OTRA_CLAVE_USUARIO),
        (C.OTRO_NOMBRE_USUARIO, C.CLAVE_USUARIO)
    )
    @unpack
    def test_retornar_error_cuando_usuario_o_clave_incorrecta(self, usuario: str, clave: str):
        sut = ControladorLogin(self.__db_con_usuario)
        sut.login(usuario, clave)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLogin.LOGIN_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_cuando_base_esta_vacia(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        sut = ControladorLogin(db)
        sut.login(C.NOMBRE_USUARIO, C.CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLogin.LOGIN_INVALIDO, respuesta["mensaje"])

    @data(
        ("", C.CLAVE_USUARIO, ServicioLogin.SIN_USUARIO),
        (None, C.CLAVE_USUARIO, ServicioLogin.SIN_USUARIO),
        (C.NOMBRE_USUARIO, "", ServicioLogin.SIN_CLAVE),
        (C.NOMBRE_USUARIO, None, ServicioLogin.SIN_CLAVE)
    )
    @unpack
    def test_retornar_error_cuando_falta_dato(self, usuario: str, clave: str, mensaje_error: str):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()
        sut = ControladorLogin(db)
        sut.login(usuario, clave)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])

    def test_retornar_ok_cuando_mail_existe_en_base_de_datos(self):
        sut = ControladorLogin(self.__db_con_usuario)
        sut.recordar(C.EMAIL_USUARIO, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorLogin.RECORDATORIO_EXITOSO, respuesta["mensaje"])

    def test_retornar_ok_cuando_mail_no_existe_en_base_de_datos(self):
        sut = ControladorLogin(self.__db_con_usuario)
        sut.recordar(C.OTRO_EMAIL_USUARIO, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ControladorLogin.RECORDATORIO_EXITOSO, respuesta["mensaje"])

    def test_retornar_ok_cuando_base_esta_vacia(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()
        sut = ControladorLogin(db)
        sut.recordar(C.OTRO_EMAIL_USUARIO, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ControladorLogin.RECORDATORIO_EXITOSO, respuesta["mensaje"])

    def test_enviar_mail_cuando_email_existe(self):
        sut = EmailSenderSpy()
        controlador = ControladorLogin(self.__db_con_usuario)
        controlador.recordar(C.EMAIL_USUARIO, sut)
        self.assertTrue(sut.envio_mail())

    def test_no_enviar_mail_cuando_email_no_existe(self):
        sut = EmailSenderSpy()
        controlador = ControladorLogin(self.__db_con_usuario)
        controlador.recordar(C.OTRO_EMAIL_USUARIO, sut)
        self.assertFalse(sut.envio_mail())

    @data(None, "")
    def test_retornar_error_cuando_el_mail_es_invalido(self, mail_invalido):
        sut = ControladorLogin(self.__db_con_usuario)
        sut.recordar(mail_invalido, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLogin.RECORDAR_SIN_MAIL, respuesta["mensaje"])

    def test_retornar_error_cuando_el_sender_es_invalido(self):
        sut = ControladorLogin(self.__db_con_usuario)
        sut.recordar("mail@mail.com", None)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLogin.RECORDAR_SIN_SENDER, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()
