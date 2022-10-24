import unittest
from ddt import ddt, data, unpack
from controller.usuario import UsuarioController
from model.tipo_usuario import TipoDeUsuario
from model.base_temporal import UsuariosFake, CreadorDeBasesDeDatosTemporales

@ddt
class UsuarioControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake({
                "Roberto": {
                    "nombre": "Roberto",
                    "apellido": "Perez",
                    "email": "roberto@gmail.com",
                    "usuario": "Roberto",
                    "clave": "123456",
                    "nacimiento": 9/17/2000,
                    "tipo": TipoDeUsuario.Pujador.value
                }})) \
            .construir()

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_usuario_ya_existente(self, tipo):
        sut = UsuarioController(self.__db_con_usuario, "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000", tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(UsuarioController.CUENTA_YA_EXISTE, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_con_email_ya_existente(self, tipo):
        sut = UsuarioController(self.__db_con_usuario, "Roberto", "Perez", "roberto@gmail.com", "Roberto1", "123456", "1/1/2000", tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(UsuarioController.CUENTA_YA_EXISTE, respuesta["mensaje"])
        
    @data(
        ("", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000", TipoDeUsuario.Consignatario, UsuarioController.SIN_NOMBRE),
        (None, "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000", TipoDeUsuario.Martillero, UsuarioController.SIN_NOMBRE),
        ("Roberto", "", "rperez@gmail.com", "Roberto", "123456", "1/1/2000", TipoDeUsuario.Pujador, UsuarioController.SIN_APELLIDO),
        ("Roberto", None, "rperez@gmail.com", "Roberto", "123456", "1/1/2000", TipoDeUsuario.Consignatario, UsuarioController.SIN_APELLIDO),
        ("Roberto", "Perez", "", "Roberto", "123456", "1/1/2000", TipoDeUsuario.Martillero, UsuarioController.SIN_EMAIL),
        ("Roberto", "Perez", None, "Roberto", "123456", "1/1/2000", TipoDeUsuario.Pujador, UsuarioController.SIN_EMAIL),
        ("Roberto", "Perez", "rperez@gmail.com", "", "123456", "1/1/2000", TipoDeUsuario.Consignatario, UsuarioController.SIN_USUARIO),
        ("Roberto", "Perez", "rperez@gmail.com", None, "123456", "1/1/2000", TipoDeUsuario.Martillero, UsuarioController.SIN_USUARIO),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", "", "1/1/2000", TipoDeUsuario.Pujador, UsuarioController.SIN_CLAVE),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", None, "1/1/2000", TipoDeUsuario.Consignatario, UsuarioController.SIN_CLAVE),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "", TipoDeUsuario.Martillero, UsuarioController.SIN_NACIMIENTO),
        ("Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", None, TipoDeUsuario.Pujador, UsuarioController.SIN_NACIMIENTO),
    )
    @unpack
    def test_retornar_error_cuando_falta_algun_dato(self, nombre, apellido, email, usuario, clave, nacimiento, tipo, mensaje_error):
        sut = UsuarioController(self.__db_con_usuario, nombre, apellido, email, usuario, clave, nacimiento, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_ese_usuario_no_existe(self, tipo):
        sut = UsuarioController(self.__db_con_usuario, "Roberto", "Perez", "rperez1@gmail.com", "Roberto1", "123456", "1/1/2000", tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(UsuarioController.CUENTA_CREADA, respuesta["mensaje"])
        
    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_base_vacia(self, tipo):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosFake({})) \
            .construir()

        sut = UsuarioController(db, "Roberto", "Perez", "rperez@gmail.com", "Roberto", "123456", "1/1/2000", tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(UsuarioController.CUENTA_CREADA, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()