import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.articulo import ControladorArticulo
from services.articulos import ServicioArticulos
from services.subastas import ServicioSubasta
from services.lotes import ServicioLote
from model.content_provider.memory import CreadorDeBasesDeDatosTemporales
from model.content_provider.memory import ArticulosEnMemoria, SubastasEnMemoria, UsuariosEnMemoria
from model.tipo_usuario import TipoDeUsuario


@ddt
class ControladorArticuloTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({
                C.NOMBRE_USUARIO: {
                    "id": 1,
                    "nombre": C.NOMBRE_USUARIO,
                    "apellido": C.APELLIDO_USUARIO,
                    "email": C.EMAIL_USUARIO,
                    "usuario": C.NOMBRE_USUARIO,
                    "clave": C.CLAVE_USUARIO,
                    "nacimiento": C.FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Consignatario
                }})) \
            .con_subastas(SubastasEnMemoria([])) \
            .con_articulos(ArticulosEnMemoria([])) \
            .construir()

    @data("", None)
    def test_retornar_error_creando_articulo_con_titulo_invalido(self, titulo_invalido):
        sut = ControladorArticulo(self.__db)
        sut.agregar(titulo_invalido, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.TITULO_INVALIDO, respuesta["mensaje"])

    @data("", None)
    def test_retornar_error_creando_articulo_con_descripcion_invalida(self, descripcion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, descripcion_invalida, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.DESCRIPCION_INVALIDA, respuesta["mensaje"])

    @data("", None, -1, 0)
    def test_retornar_error_creando_articulo_con_valuacion_invalida(self, valuacion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, valuacion_invalida, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.VALUACION_INVALIDA, respuesta["mensaje"])

    @data("", None, -1, 0)
    def test_retornar_error_creando_articulo_con_consignatario_invalido(self, consignatario_invalido):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, consignatario_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.CONSIGNATARIO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_creando_articulo_con_consignatario_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.CONSIGNATARIO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_ok_al_crear_correctamente(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorArticulo.ARTICULO_CREADO, respuesta["mensaje"])

    def test_crear_articulo_con_datos_correctos(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        articulo = self.__db.Articulos.buscar_por_uid(1)
        self.assertEqual(1, articulo.obtener_uid())
        self.assertEqual(C.TITULO_ARTICULO, articulo.obtener_titulo())
#        self.assertEqual(C.DESCRIPCION_ARTICULO, articulo.obtener_descripcion())
#        self.assertEqual(C.VALUACION_ARTICULO, articulo.obtener_valuacion())
        self.assertEqual(1, articulo.obtener_consignatario_uid())

    def test_retornar_articulo_al_buscar_articulo_creado(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.buscar_por_uid(1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual({"consignatario_id": 1, "id": 1, "titulo": "Sofa Antiguo",
                          "descripcion": "Un sofa de principios de siglo.", "valuacion": 15000}, respuesta["item"])

    @data(None, "", -1, 0)
    def test_retornar_error_al_buscar_articulo_invalido(self, uid_invalido):
        sut = ControladorArticulo(self.__db)
        sut.buscar_por_uid(uid_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.UID_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_al_buscar_articulo_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.buscar_por_uid(C.OTRO_ARTICULO_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_articulos_al_buscar_por_consignatario_existente_con_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.agregar(C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        sut.listar_articulos_propiedad_de(1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, len(respuesta["items"]))
        self.assertIn({"id": 1, "consignatario_id": 1, "titulo": "Sofa Antiguo",
                       "descripcion": "Un sofa de principios de siglo.", "valuacion": 15000}, respuesta["items"])
        self.assertIn({"id": 2, "consignatario_id": 1, "titulo": "Reloj de Arena",
                       "descripcion": "Un reloj de arena que atrasa.", "valuacion": 3000}, respuesta["items"])

    def test_retonar_vacio_al_buscar_por_consignatario_existente_sin_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.listar_articulos_propiedad_de(1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([], respuesta["items"])

    @data(None, "", -1, 0)
    def test_retornar_error_al_buscar_por_consignatario_invalido(self, uid_invalido):
        sut = ControladorArticulo(self.__db)
        sut.listar_articulos_propiedad_de(uid_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.LISTAR_CON_CONSIGNATARIO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_al_buscar_por_consignatario_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.listar_articulos_propiedad_de(C.OTRO_ID_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.LISTAR_CON_CONSIGNATARIO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_ok_cuando_se_cuenta_sin_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.contar()
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(0, respuesta["total"])

    def test_retornar_ok_cuando_se_cuenta_con_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.agregar(C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        sut.contar()
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["total"])

    def test_retornar_error_cuando_hay_error_interno_al_contar(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_articulos(None) \
            .construir()
        sut = ControladorArticulo(db)
        sut.contar()
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertNotEqual("", respuesta["mensaje"])

    @data(None, "", -1, 0)
    def test_retornar_error_cuando_se_borra_articulo_invalido(self, articulo_invalido):
        sut = ControladorArticulo(self.__db)
        sut.borrar(articulo_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.BORRAR_ARTICULO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_cuando_se_borra_articulo_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.borrar(C.ARTICULO_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.BORRAR_ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_se_borra_articulo_en_lote(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        subasta_uid = ServicioSubasta(self.__db).crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                       C.FECHA_DE_SUBASTA)
        ServicioLote(self.__db).agregar(subasta_uid, C.ARTICULO_UID, C.BASE_LOTE, C.ORDEN_LOTE)
        sut.borrar(C.ARTICULO_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.BORRAR_ARTICULO_EN_LOTE, respuesta["mensaje"])

    def test_borrar_articulo_correctamente_cuando_no_hay_lotes(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.borrar(C.ARTICULO_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorArticulo.ARTICULO_BORRADO, respuesta["mensaje"])

    def test_borrar_articulo_correctamente_cuando_no_esta_en_ningun_lote(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        subasta_uid = ServicioSubasta(self.__db).crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                       C.FECHA_DE_SUBASTA)
        ServicioLote(self.__db).agregar(subasta_uid, C.ARTICULO_UID, C.BASE_LOTE, C.ORDEN_LOTE)
        sut.agregar(C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        sut.borrar(C.OTRO_ARTICULO_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorArticulo.ARTICULO_BORRADO, respuesta["mensaje"])

    def test_listar_vacio_cuando_no_hay_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.listar()
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([], respuesta["items"])

    def test_listar_elementos_cuando_hay_articulos(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.agregar(C.OTRO_ARTICULO_UID, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        sut.listar()
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, len(respuesta["items"]))
        self.assertIn({
            "consignatario_id": 1,
            "descripcion": "Un sofa de principios de siglo.",
            "id": 1,
            "titulo": "Sofa Antiguo",
            "valuacion": 15000}, respuesta["items"])
        self.assertIn({
            "consignatario_id": 1,
            "descripcion": "Un reloj de arena que atrasa.",
            "id": 2,
            "titulo": 2,
            "valuacion": 3000}, respuesta["items"])
        sut.listar()

    def test_retornar_error_cuando_ocurre_un_error_interno(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_articulos(None) \
            .construir()
        sut = ControladorArticulo(db)
        sut.listar()
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertNotEqual("", respuesta["mensaje"])

    @data(None, "", -1, 0)
    def test_retornar_error_actualizando_articulo_invalido(self, articulo_invalido):
        sut = ControladorArticulo(self.__db)
        sut.actualizar(articulo_invalido, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.UID_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_actualizando_articulo_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.actualizar(C.OTRO_ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.ACTUALIZANDO_ARTICULO_INEXISTENTE, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_con_titulo_invalido(self, titulo_invalido):
        sut = ControladorArticulo(self.__db)
        sut.actualizar(C.OTRO_ARTICULO_UID, titulo_invalido, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.TITULO_INVALIDO, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_con_descripcion_invalida(self, descripcion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.actualizar(C.OTRO_ARTICULO_UID, C.OTRO_TITULO_ARTICULO, descripcion_invalida, C.OTRA_VALUACION_ARTICULO, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.DESCRIPCION_INVALIDA, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_con_valuacion_invalida(self, valuacion_invalida):
        sut = ControladorArticulo(self.__db)
        sut.actualizar(C.OTRO_ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, valuacion_invalida, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.VALUACION_INVALIDA, respuesta["mensaje"])

    @data(None, "")
    def test_retornar_error_actualizando_con_consignatario_invalido(self, consignatario_invalido):
        sut = ControladorArticulo(self.__db)
        sut.actualizar(C.OTRO_ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO,
                       consignatario_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.CONSIGNATARIO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_actualizando_con_consignatario_inexistente(self):
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.actualizar(C.ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioArticulos.CONSIGNATARIO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_ok_cuando_se_actualiza_correctamente(self):
        self.__db.Usuarios.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                                   C.OTRA_CLAVE_USUARIO, C.OTRA_FECHA_SUBASTA, TipoDeUsuario.Consignatario)
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.actualizar(C.ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorArticulo.ARTICULO_ACTUALIZADO, respuesta["mensaje"])

    def test_retornar_ok_cuando_se_actualiza_correctamente_entre_varios_articulos(self):
        self.__db.Usuarios.agregar(C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                                   C.OTRA_CLAVE_USUARIO, C.OTRA_FECHA_SUBASTA, TipoDeUsuario.Consignatario)
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.agregar("Cama estilo Imperio", "Cama estilo Imperio de 3 plazas y media", 12400, 1)
        sut.actualizar(C.ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorArticulo.ARTICULO_ACTUALIZADO, respuesta["mensaje"])

    def test_actualizar_datos_correctamente(self):
        self.__db.Usuarios.agregar(C.OTRO_NOMBRE_USUARIO, C.OTRO_APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO,
                                   C.OTRA_CLAVE_USUARIO, C.OTRA_FECHA_SUBASTA, TipoDeUsuario.Consignatario)
        sut = ControladorArticulo(self.__db)
        sut.agregar(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, 1)
        sut.actualizar(C.ARTICULO_UID, C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO, 2)

        articulo = self.__db.Articulos.buscar_por_uid(1)
        self.assertEqual(C.OTRO_TITULO_ARTICULO, articulo.obtener_titulo())
        self.assertEqual(C.OTRA_DESCRIPCION_ARTICULO, articulo.obtener_descripcion())
        self.assertEqual(C.OTRA_VALUACION_ARTICULO, articulo.obtener_valuacion())
        self.assertEqual(2, articulo.obtener_consignatario_uid())


if __name__ == "__main__":
    unittest.main()
