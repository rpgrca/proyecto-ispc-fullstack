import unittest
from ddt import ddt, data, unpack
import tests.constantes as C
from controller.usuario import ServicioUsuario
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class ServicioUsuarioTests(unittest.TestCase):
    def setUp(self):
        self.__db_con_usuario = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({
                C.NOMBRE_USUARIO: {
                    "id": C.ID_USUARIO,
                    "nombre": C.NOMBRE_USUARIO,
                    "apellido": C.APELLIDO_USUARIO,
                    "email": C.EMAIL_USUARIO,
                    "usuario": C.NOMBRE_USUARIO,
                    "clave": C.CLAVE_USUARIO,
                    "nacimiento": C.FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Pujador.value
                }})) \
            .construir()

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_usuario_ya_existente(self, tipo):
        sut = ServicioUsuario(self.__db_con_usuario, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO,
                              C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CUENTA_YA_EXISTE, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_con_email_ya_existente(self, tipo):
        sut = ServicioUsuario(self.__db_con_usuario, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.EMAIL_USUARIO,
                              "Roberto1", C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CUENTA_YA_EXISTE, respuesta["mensaje"])

    @data(
        ("", C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, ServicioUsuario.SIN_NOMBRE),
        (None, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Martillero, ServicioUsuario.SIN_NOMBRE),
        (C.NOMBRE_USUARIO, "", C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Pujador, ServicioUsuario.SIN_APELLIDO),
        (C.NOMBRE_USUARIO, None, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, ServicioUsuario.SIN_APELLIDO),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, "", C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Martillero, ServicioUsuario.SIN_EMAIL),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, None, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Pujador, ServicioUsuario.SIN_EMAIL),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, "", C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, ServicioUsuario.SIN_USUARIO),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, None, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Martillero, ServicioUsuario.SIN_USUARIO),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, "", C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Pujador, ServicioUsuario.SIN_CLAVE),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, None, C.FECHA_NACIMIENTO_USUARIO,
         TipoDeUsuario.Consignatario, ServicioUsuario.SIN_CLAVE),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, "",
         TipoDeUsuario.Martillero, ServicioUsuario.SIN_NACIMIENTO),
        (C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO, None,
         TipoDeUsuario.Pujador, ServicioUsuario.SIN_NACIMIENTO),
    )
    @unpack
    def test_retornar_error_cuando_falta_algun_dato(self, nombre, apellido, email, usuario, clave, nacimiento, tipo,
                                                    mensaje_error):
        sut = ServicioUsuario(self.__db_con_usuario, nombre, apellido, email, usuario, clave, nacimiento, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_ese_usuario_no_existe(self, tipo):
        sut = ServicioUsuario(self.__db_con_usuario, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, "rperez1@gmail.com",
                              "Roberto1", C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ServicioUsuario.CUENTA_CREADA, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_base_vacia(self, tipo):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        sut = ServicioUsuario(db, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO,
                              C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ServicioUsuario.CUENTA_CREADA, respuesta["mensaje"])

    def test_completar_usuario_correctamente(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        ServicioUsuario(db, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO,
                        C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)
        usuario = db.Usuarios.buscar(C.NOMBRE_USUARIO, C.CLAVE_USUARIO)

        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(C.APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(C.OTRO_EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(C.FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())


if __name__ == "__main__":
    unittest.main()
