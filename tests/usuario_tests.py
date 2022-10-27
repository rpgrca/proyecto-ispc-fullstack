import unittest
from ddt import ddt, data, unpack
from tests.constantes import *
from controller.usuario import UsuarioController
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class UsuarioControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({
                NOMBRE_USUARIO: {
                    "id": ID_USUARIO,
                    "nombre": NOMBRE_USUARIO,
                    "apellido": APELLIDO_USUARIO,
                    "email": EMAIL_USUARIO,
                    "usuario": NOMBRE_USUARIO,
                    "clave": CLAVE_USUARIO,
                    "nacimiento": FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Pujador.value
                }})) \
            .construir()

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_usuario_ya_existente(self, tipo):
        sut = UsuarioController(self.__db_con_usuario, NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO,
                                NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(UsuarioController.CUENTA_YA_EXISTE, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_con_email_ya_existente(self, tipo):
        sut = UsuarioController(self.__db_con_usuario, NOMBRE_USUARIO, APELLIDO_USUARIO, EMAIL_USUARIO,
                                "Roberto1", CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(UsuarioController.CUENTA_YA_EXISTE, respuesta["mensaje"])

    @data(
        ("", APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, UsuarioController.SIN_NOMBRE),
        (None, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Martillero, UsuarioController.SIN_NOMBRE),
        (NOMBRE_USUARIO, "", OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Pujador, UsuarioController.SIN_APELLIDO),
        (NOMBRE_USUARIO, None, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, UsuarioController.SIN_APELLIDO),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, "", NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Martillero, UsuarioController.SIN_EMAIL),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, None, NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Pujador, UsuarioController.SIN_EMAIL),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, "", CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, UsuarioController.SIN_USUARIO),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, None, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Martillero, UsuarioController.SIN_USUARIO),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, "", FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Pujador, UsuarioController.SIN_CLAVE),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, None, FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, UsuarioController.SIN_CLAVE),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, "",
         TipoDeUsuario.Martillero, UsuarioController.SIN_NACIMIENTO),
        (NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO, CLAVE_USUARIO, None,
         TipoDeUsuario.Pujador, UsuarioController.SIN_NACIMIENTO),
    )
    @unpack
    def test_retornar_error_cuando_falta_algun_dato(self, nombre, apellido, email, usuario, clave, nacimiento, tipo,
                                                    mensaje_error):
        sut = UsuarioController(self.__db_con_usuario, nombre, apellido, email, usuario, clave, nacimiento, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_ese_usuario_no_existe(self, tipo):
        sut = UsuarioController(self.__db_con_usuario, NOMBRE_USUARIO, APELLIDO_USUARIO, "rperez1@gmail.com",
                                "Roberto1", CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(UsuarioController.CUENTA_CREADA, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_base_vacia(self, tipo):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        sut = UsuarioController(db, NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO,
                                NOMBRE_USUARIO, CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(UsuarioController.CUENTA_CREADA, respuesta["mensaje"])

    def test_completar_usuario_correctamente(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        UsuarioController(db, NOMBRE_USUARIO, APELLIDO_USUARIO, OTRO_EMAIL_USUARIO, NOMBRE_USUARIO,
                          CLAVE_USUARIO, FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)
        usuario = db.Usuarios.buscar(NOMBRE_USUARIO, CLAVE_USUARIO)

        self.assertEqual(NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(OTRO_EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())


if __name__ == "__main__":
    unittest.main()
