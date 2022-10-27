import unittest
from ddt import ddt
import tests.constantes as C
from controller.email_sender import EmailSender
from controller.reestablecer import ServicioController
from model.tipo_usuario import TipoDeUsuario
from model.usuarios import Usuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


class EmailSenderSpy(EmailSender):
    def __init__(self):
        self.__enviado = False

    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        self.__enviado = True

    def envio_mail(self) -> bool:
        return self.__enviado


@ddt
class ServicioReestablecerTests(unittest.TestCase):
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

    def test_retornar_ok_cuando_mail_existe_en_base_de_datos(self):
        sut = ServicioController(self.__db_con_usuario, C.EMAIL_USUARIO, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ServicioController.RECORDATORIO_EXITOSO, respuesta["mensaje"])

    def test_retornar_ok_cuando_mail_no_existe_en_base_de_datos(self):
        sut = ServicioController(self.__db_con_usuario, C.OTRO_EMAIL_USUARIO, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ServicioController.RECORDATORIO_EXITOSO, respuesta["mensaje"])

    def test_retornar_ok_cuando_base_esta_vacia(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()
        sut = ServicioController(db, C.OTRO_EMAIL_USUARIO, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ServicioController.RECORDATORIO_EXITOSO, respuesta["mensaje"])

    def test_enviar_mail_cuando_email_existe(self):
        sut = EmailSenderSpy()
        ServicioController(self.__db_con_usuario, C.EMAIL_USUARIO, sut).obtener_respuesta()
        self.assertTrue(sut.envio_mail())

    def test_no_enviar_mail_cuando_email_no_existe(self):
        sut = EmailSenderSpy()
        ServicioController(self.__db_con_usuario, C.OTRO_EMAIL_USUARIO, sut).obtener_respuesta()
        self.assertFalse(sut.envio_mail())


if __name__ == "__main__":
    unittest.main()
