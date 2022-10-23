import unittest
from controller.registro import RegistroController
from model.tipo_usuario import TipoDeUsuario
from model.usuarios import UsuariosImplementadoConDiccionario

class RegistroControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_pujador(self):
        dictionary = {}
        RegistroController(UsuariosImplementadoConDiccionario(dictionary), "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000")
        self.assertEqual(TipoDeUsuario.Pujador.value, dictionary["Roberto"]["tipo"])


if __name__ == "__main__":
    unittest.main()