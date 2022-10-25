import unittest
from controller.registro import RegistroController
from model.tipo_usuario import TipoDeUsuario
from model.base_temporal import UsuariosFake, CreadorDeBasesDeDatosTemporales


class RegistroControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_pujador(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake(diccionario)) \
            .construir()

        RegistroController(db, "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", 1/1/2000)
        self.assertEqual(TipoDeUsuario.Pujador.value, diccionario["Roberto"]["tipo"])


if __name__ == "__main__":
    unittest.main()
