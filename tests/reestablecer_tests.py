import unittest
from ddt import ddt
from controller.reestablecer import ReestablecerController, EmailSender
from model.tipo_usuario import TipoDeUsuario
from model.usuarios import UsuariosImplementadoConDiccionario, Usuario


class EmailSenderSpy(EmailSender):
    def __init__(self):
        self.__enviado = False
    
    def enviar_mail_a(self, usuario: Usuario, mensaje: str) -> None:
        self.__enviado = True

    def envio_mail(self) -> bool:
        return self.__enviado


@ddt
class ReestablecerControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = UsuariosImplementadoConDiccionario({
            "Roberto": {
                "nombre": "Roberto",
                "apellido": "Perez",
                "email": "roberto@gmail.com",
                "usuario": "Roberto",
                "clave": "123456",
                "nacimiento": 9/17/2000,
                "tipo": TipoDeUsuario.Pujador.value
            }
        })


    def test_retornar_ok_cuando_mail_existe_en_base_de_datos(self):
        sut = ReestablecerController(self.__db_con_usuario, "roberto@gmail.com", EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_retornar_ok_cuando_mail_no_existe_en_base_de_datos(self):
        sut = ReestablecerController(self.__db_con_usuario, "rperez@gmail.com", EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_retornar_ok_cuando_base_esta_vacia(self):
        sut = ReestablecerController(UsuariosImplementadoConDiccionario({}), "rperez@gmail.com", EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_enviar_mail_cuando_email_existe(self):
        sut = EmailSenderSpy()
        ReestablecerController(self.__db_con_usuario, "roberto@gmail.com", sut).obtener_respuesta()
        self.assertTrue(sut.envio_mail())


    def test_no_enviar_mail_cuando_email_no_existe(self):
        sut = EmailSenderSpy()
        ReestablecerController(self.__db_con_usuario, "rperez@gmail.com", sut).obtener_respuesta()
        self.assertFalse(sut.envio_mail())


if __name__ == "__main__":
    unittest.main()