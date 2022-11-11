import unittest
from ddt import ddt, data, unpack
import tests.constantes as C
from tests.email_sender_spy import EmailSenderSpy
from model.usuarios import Consignatario, Martillero, Pujador, Usuarios
from controller.usuario import ControladorUsuario, ServicioUsuario
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class ControladorUsuarioTests(unittest.TestCase):
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
                    "tipo": TipoDeUsuario.Pujador
                }})) \
            .construir()

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_usuario_ya_existente(self, tipo):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO,
                    C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CUENTA_YA_EXISTE, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_error_cuando_quiere_crear_con_email_ya_existente(self, tipo):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.EMAIL_USUARIO,
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
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(nombre, apellido, email, usuario, clave, nacimiento, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])

    def test_graba_usuario_de_tipo_pujador(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria(diccionario)) \
            .construir()

        sut = ControladorUsuario(db)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO,
                    C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)
        self.assertEqual(TipoDeUsuario.Pujador, diccionario[C.NOMBRE_USUARIO]["tipo"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_ese_usuario_no_existe(self, tipo):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, "rperez1@gmail.com",
                    "Roberto1", C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ControladorUsuario.CUENTA_CREADA, respuesta["mensaje"])

    @data(TipoDeUsuario.Martillero, TipoDeUsuario.Consignatario, TipoDeUsuario.Pujador)
    def test_retornar_ok_cuando_base_vacia(self, tipo):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        sut = ControladorUsuario(db)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO,
                    C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn(ControladorUsuario.CUENTA_CREADA, respuesta["mensaje"])

    def test_completar_usuario_correctamente(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({})) \
            .construir()

        sut = ControladorUsuario(db)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO,
                    C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)
        usuario = db.Usuarios.buscar(C.NOMBRE_USUARIO, C.CLAVE_USUARIO)

        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(C.APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(C.OTRO_EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(C.FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())

    @data(
        (TipoDeUsuario.Martillero, Martillero),
        (TipoDeUsuario.Consignatario, Consignatario),
        (TipoDeUsuario.Pujador, Pujador)
    )
    @unpack
    def test_retorna_instancia_martillero_cuando_se_pide_crear_martillero(self, tipo: TipoDeUsuario, clase: type):
        usuario = Usuarios.crear(C.ID_USUARIO, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.EMAIL_USUARIO,
                                 C.NOMBRE_USUARIO, C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, tipo)
        self.assertIsInstance(usuario, clase)

    def test_retornar_ok_cuando_actualiza_usuario(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorUsuario.CUENTA_ACTUALIZADA, respuesta["mensaje"])

    def test_actualizar_datos_correctamente(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        usuario = self.__db_con_usuario.Usuarios.buscar_usuario_por_uid(C.ID_USUARIO)
        self.assertEqual(C.ID_USUARIO, usuario.obtener_uid())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(C.APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(C.OTRO_EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(C.OTRO_NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(C.OTRA_CLAVE_USUARIO, usuario.obtener_clave())
        self.assertEqual(C.FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())
        self.assertEqual(TipoDeUsuario.Pujador, usuario.obtener_tipo())

    def test_actualizar_datos_correctamente_cuando_mantiene_usuario(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        usuario = self.__db_con_usuario.Usuarios.buscar_usuario_por_uid(C.ID_USUARIO)
        self.assertEqual(C.ID_USUARIO, usuario.obtener_uid())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(C.APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(C.OTRO_EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(C.OTRA_CLAVE_USUARIO, usuario.obtener_clave())
        self.assertEqual(C.FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())
        self.assertEqual(TipoDeUsuario.Pujador, usuario.obtener_tipo())

    def test_actualizar_datos_correctamente_cuando_mantiene_email(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        usuario = self.__db_con_usuario.Usuarios.buscar_usuario_por_uid(C.ID_USUARIO)
        self.assertEqual(C.ID_USUARIO, usuario.obtener_uid())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(C.APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(C.EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(C.OTRO_NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(C.OTRA_CLAVE_USUARIO, usuario.obtener_clave())
        self.assertEqual(C.FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())
        self.assertEqual(TipoDeUsuario.Pujador, usuario.obtener_tipo())

    def test_actualizar_datos_correctamente_cuando_mantiene_password(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.EMAIL_USUARIO, C.CLAVE_USUARIO)
        usuario = self.__db_con_usuario.Usuarios.buscar_usuario_por_uid(C.ID_USUARIO)
        self.assertEqual(C.ID_USUARIO, usuario.obtener_uid())
        self.assertEqual(C.NOMBRE_USUARIO, usuario.obtener_nombre())
        self.assertEqual(C.APELLIDO_USUARIO, usuario.obtener_apellido())
        self.assertEqual(C.EMAIL_USUARIO, usuario.obtener_email())
        self.assertEqual(C.OTRO_NOMBRE_USUARIO, usuario.obtener_usuario())
        self.assertEqual(C.CLAVE_USUARIO, usuario.obtener_clave())
        self.assertEqual(C.FECHA_NACIMIENTO_USUARIO, usuario.obtener_nacimiento())
        self.assertEqual(TipoDeUsuario.Pujador, usuario.obtener_tipo())

    @data(None, "", -1, 0)
    def test_retornar_error_actualizando_usuario_invalido(self, usuario_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(usuario_invalido, C.OTRO_NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.USUARIO_UID_INVALIDO, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_usuario_con_nombre_invalido(self, usuario_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, usuario_invalido, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.USUARIO_INVALIDO, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_usuario_con_email_invalido(self, email_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, email_invalido, C.OTRA_CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.EMAIL_INVALIDO, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_usuario_con_clave_invalida(self, clave_invalida):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, clave_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CLAVE_INVALIDA, respuesta["mensaje"])

    def test_retornar_error_cuando_usuario_no_existe(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.actualizar(C.OTRO_ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.USUARIO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_nombre_de_usuario_ya_existe(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Consignatario)
        sut.actualizar(C.ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRA_CLAVE_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.USUARIO_YA_EXISTE, respuesta["mensaje"])

    def test_retornar_ok_al_contactar_correctamente_al_martillero(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(C.NOMBRE_USUARIO, C.EMAIL_USUARIO, "asunto corto", "texto largo", EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorUsuario.MENSAJE_ENVIADO, respuesta["mensaje"])

    def test_enviar_mail_correctamente(self):
        spy = EmailSenderSpy()
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(C.NOMBRE_USUARIO, C.EMAIL_USUARIO, C.ASUNTO_MENSAJE, C.TEXTO_MENSAJE, spy)
        self.assertTrue(spy.envio_mail())
        self.assertIn(C.NOMBRE_USUARIO, spy.mensaje_enviado())
        self.assertIn(C.EMAIL_USUARIO, spy.mensaje_enviado())
        self.assertIn(C.ASUNTO_MENSAJE, spy.mensaje_enviado())
        self.assertIn(C.TEXTO_MENSAJE, spy.mensaje_enviado())

    def test_retornar_error_cuando_sender_es_invalido(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(C.NOMBRE_USUARIO, C.EMAIL_USUARIO, C.ASUNTO_MENSAJE, C.TEXTO_MENSAJE, None)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.SENDER_INVALIDO, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_cuando_usuario_es_invalido(self, usuario_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(usuario_invalido, C.EMAIL_USUARIO, C.ASUNTO_MENSAJE, C.TEXTO_MENSAJE, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CONTACTO_SIN_NOMBRE, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_cuando_email_es_invalido(self, email_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(C.NOMBRE_USUARIO, email_invalido, C.ASUNTO_MENSAJE, C.TEXTO_MENSAJE, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CONTACTO_SIN_EMAIL, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_cuando_asunto_es_invalido(self, asunto_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(C.NOMBRE_USUARIO, C.EMAIL_USUARIO, asunto_invalido, C.TEXTO_MENSAJE, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CONTACTO_SIN_ASUNTO, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_cuando_texto_es_invalido(self, texto_invalido):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                    C.OTRA_CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Martillero)
        sut.contactar(C.NOMBRE_USUARIO, C.EMAIL_USUARIO, C.ASUNTO_MENSAJE, texto_invalido, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.CONTACTO_SIN_TEXTO, respuesta["mensaje"])

    def test_retornar_error_cuando_martillero_no_existe(self):
        sut = ControladorUsuario(self.__db_con_usuario)
        sut.contactar(C.NOMBRE_USUARIO, C.EMAIL_USUARIO, C.ASUNTO_MENSAJE, C.TEXTO_MENSAJE, EmailSenderSpy())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioUsuario.MARTILLERO_INEXISTENTE, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()
