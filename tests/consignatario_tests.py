import unittest
from controller.consignatario import ConsignatarioController
from model.usuarios import TipoDeUsuario, UsuariosImplementadoConDiccionario

class ConsignatarioControllerTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_pujador(self):
        dictionary = {}
        ConsignatarioController(UsuariosImplementadoConDiccionario(dictionary), "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000")
        self.assertEqual(TipoDeUsuario.Consignatario.value, dictionary["Roberto"]["tipo"])


if __name__ == "__main__":
    unittest.main()