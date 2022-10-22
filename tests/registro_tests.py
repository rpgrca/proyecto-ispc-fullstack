import unittest
from ddt import ddt, data, unpack
from controller.registro import RegistroController
from model.usuarios import UsuariosImplementadoConDiccionario

@ddt
class RegistroControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = UsuariosImplementadoConDiccionario({
            "Roberto": { "clave": "123456", "email": "roberto@gmail.com" }
        })


    def test_retornar_error_cuando_quiere_crear_usuario_ya_existente(self):
        respuesta = RegistroController(self.__db_con_usuario, "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000").obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("La cuenta ya existe", respuesta["mensaje"])
        
    
    def test_retornar_error_cuando_quiere_crear_con_email_ya_existente(self):
        respuesta = RegistroController(self.__db_con_usuario, "Roberto", "Perez", "roberto@gmail.com", "Roberto1", "123456", "1/1/2000").obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("La cuenta ya existe", respuesta["mensaje"])
        
        
    @data(
        ("", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000"),
        (None, "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000"),
        ("Roberto", "", "rperez@gmail.com", "Roberto", "123456", "1/1/2000"),
        ("Roberto", None, "rperez@gmail.com", "Roberto", "123456", "1/1/2000"),
        ("Roberto", "Perez", "", "Roberto", "123456", "1/1/2000"),
        ("Roberto", "Perez", None, "Roberto", "123456", "1/1/2000"),
        ("Roberto", "Perez", "rperez@gmail.com", "", "123456", "1/1/2000"),
        ("Roberto", "Perez", "rperez@gmail.com", None, "123456", "1/1/2000"),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", "", "1/1/2000"),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", None, "1/1/2000"),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", ""),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", None),
    )
    @unpack
    def test_retornar_error_cuando_falta_algun_dato(self, nombre: str, apellido: str, email: str, usuario: str, clave: str, nacimiento: str):
        sut = RegistroController(self.__db_con_usuario, nombre, apellido, email, usuario, clave, nacimiento)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn("No se puede crear un usuario sin", respuesta["mensaje"])


    def test_retornar_ok_cuando_ese_usuario_no_existe(self):
        sut = RegistroController(self.__db_con_usuario, "Roberto", "Perez", "rperez1@gmail.com", "Roberto1", "123456", "1/1/2000")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("La cuenta ha sido creada correctamente", respuesta["mensaje"])
        
        
    def test_retornar_ok_cuando_base_vacia(self):
        sut = RegistroController(UsuariosImplementadoConDiccionario({}), "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("La cuenta ha sido creada correctamente", respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()