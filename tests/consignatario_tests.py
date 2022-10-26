import unittest
from controller.consignatario import ConsignatarioController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosFake, CreadorDeBasesDeDatosTemporales


class ConsignatarioControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_consignatario(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake(diccionario)) \
            .construir()

        ConsignatarioController(db, "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", 1/1/2000)
        self.assertEqual(TipoDeUsuario.Consignatario.value, diccionario["Roberto"]["tipo"])


if __name__ == "__main__":
    unittest.main()
