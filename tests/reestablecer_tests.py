import unittest
from ddt import ddt
from controller.reestablecer import ReestablecerController, EmailSender
from model.usuarios import UsuariosImplementadoConDiccionario, Usuario


class FakeEmailSender(EmailSender):
    def __init__(self):
        self.__enviado = False
    
    def enviar_mail_a(self, usuario: Usuario):
        self.__enviado = True

    def envio_mail(self):
        return self.__enviado


@ddt
class ReestablecerControllerTests(unittest.TestCase):
    __db_con_usuario = UsuariosImplementadoConDiccionario({
        "Roberto": { "clave": "123456", "email": "roberto@gmail.com" }
    })


    def test_retornar_ok_cuando_mail_existe_en_base_de_datos(self):
        sut = ReestablecerController(self.__db_con_usuario, "roberto@gmail.com", FakeEmailSender())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_retornar_ok_cuando_mail_no_existe_en_base_de_datos(self):
        sut = ReestablecerController(self.__db_con_usuario, "rperez@gmail.com", FakeEmailSender())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_retornar_ok_cuando_base_esta_vacia(self):
        sut = ReestablecerController(UsuariosImplementadoConDiccionario({}), "rperez@gmail.com", FakeEmailSender())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_enviar_mail_cuando_email_existe(self):
        sut = FakeEmailSender()
        ReestablecerController(self.__db_con_usuario, "roberto@gmail.com", sut).obtener_respuesta()
        self.assertTrue(sut.envio_mail())


    def test_no_enviar_mail_cuando_email_no_existe(self):
        sut = FakeEmailSender()
        ReestablecerController(self.__db_con_usuario, "rperez@gmail.com", sut).obtener_respuesta()
        self.assertFalse(sut.envio_mail())


if __name__ == "__main__":
    unittest.main()