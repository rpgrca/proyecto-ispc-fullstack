import unittest
from controller.registro import RegistroController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


class RegistroControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_pujador(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria(diccionario)) \
            .construir()

        RegistroController(db, "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", 1/1/2000)
        self.assertEqual(TipoDeUsuario.Pujador.value, diccionario["Roberto"]["tipo"])


if __name__ == "__main__":
    unittest.main()
