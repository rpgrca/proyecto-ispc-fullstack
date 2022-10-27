import unittest
from tests.constantes import *
from controller.registro import RegistroController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


class RegistroControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_pujador(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria(diccionario)) \
            .construir()

        RegistroController(db, NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO)
        self.assertEqual(TipoDeUsuario.Pujador.value, diccionario[NOMBRE_USUARIO]["tipo"])


if __name__ == "__main__":
    unittest.main()
