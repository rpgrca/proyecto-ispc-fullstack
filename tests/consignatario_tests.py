import unittest
from tests.constantes import *
from controller.consignatario import ConsignatarioController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


class ConsignatarioControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_consignatario(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria(diccionario)) \
            .construir()

        ConsignatarioController(db, NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO)
        self.assertEqual(TipoDeUsuario.Consignatario.value, diccionario[NOMBRE_USUARIO]["tipo"])


if __name__ == "__main__":
    unittest.main()

