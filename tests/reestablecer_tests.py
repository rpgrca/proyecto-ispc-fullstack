import unittest
from ddt import ddt
from controller.reestablecer import ReestablecerController
from model.usuarios import UsuariosImplementadoConDiccionario

@ddt
class ReestablecerControllerTests(unittest.TestCase):
    __db_con_usuario = UsuariosImplementadoConDiccionario({
        "Roberto": { "clave": "123456", "email": "roberto@gmail.com" }
    })


    def test_retornar_ok_cuando_mail_existe_en_base_de_datos(self):
        sut = ReestablecerController(self.__db_con_usuario, "roberto@gmail.com")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_retornar_ok_cuando_mail_no_existe_en_base_de_datos(self):
        sut = ReestablecerController(self.__db_con_usuario, "rperez@gmail.com")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


    def test_retornar_ok_cuando_base_esta_vacia(self):
        sut = ReestablecerController(UsuariosImplementadoConDiccionario({}), "rperez@gmail.com")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("Si el correo está en nuestros registros se ha enviado un recordatorio a su cuenta", respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()   