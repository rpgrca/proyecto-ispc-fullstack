import unittest
from ddt import ddt, data
import tests.constantes as C
from model.tipo_usuario import TipoDeUsuario
from controller.lote import ControladorLote, ServicioLote
from model.articulos import Articulo
from model.subastas import Subasta
from model.content_provider.memory import CreadorDeBasesDeDatosTemporales, ArticulosEnMemoria
from model.content_provider.memory import SubastasEnMemoria, UsuariosEnMemoria


@ddt
class ControladorLoteTests(unittest.TestCase):
    def setUp(self):
        usuarios = UsuariosEnMemoria({
                "Consignatario": {
                    "id": 1,
                    "nombre": C.NOMBRE_USUARIO,
                    "apellido": C.APELLIDO_USUARIO,
                    "email": C.EMAIL_USUARIO,
                    "usuario": "Consignatario",
                    "clave": C.CLAVE_USUARIO,
                    "nacimiento": C.FECHA_NACIMIENTO_USUARIO,
                    "tipo": TipoDeUsuario.Consignatario}
            })

        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(usuarios) \
            .con_subastas(SubastasEnMemoria([Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                     C.FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([Articulo(1, C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO,
                                                        usuarios.buscar_usuario_por_uid(1))])) \
            .construir()

    @data("", None, -1, 0)
    def test_retornar_error_contando_con_subasta_invalida(self, subasta_invalida):
        sut = ControladorLote(self.__db)
        sut.contar_lotes_en(subasta_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.CONTAR_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_contando_con_subasta_inexistente(self):
        sut = ControladorLote(self.__db)
        sut.contar_lotes_en(C.OTRA_SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.CONTAR_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_retorna_la_cantidad_de_lotes_correctamente(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100, C.ORDEN_LOTE)
        sut.contar_lotes_en(C.SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["total"])

    @data("", None, -1, 0)
    def test_retornar_error_cuando_falta_subasta_en_agregar(self, lote_invalido):
        sut = ControladorLote(self.__db)
        sut.agregar(lote_invalido, C.ARTICULO_UID, 100, C.ORDEN_LOTE)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LOTE_SIN_SUBASTA, respuesta["mensaje"])

    @data("", None, -1, 0)
    def test_retornar_error_cuando_falta_articulo_en_agregar(self, articulo_invalido):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, articulo_invalido, 100, C.ORDEN_LOTE)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.ARTICULO_NULO_EN_SUBASTA, respuesta["mensaje"])

    @data("", None)
    def test_retornar_error_cuando_orden_es_invalido(self, orden_invalido):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, C.BASE_LOTE, orden_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.ORDEN_INVALIDO, respuesta["mensaje"])

    @data("", None, -1)
    def test_retornar_error_cuando_base_es_invalida(self, base_invalida):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, base_invalida, C.ORDEN_LOTE)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.BASE_INVALIDA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 100, C.ORDEN_LOTE)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.OTRA_SUBASTA_UID, C.ARTICULO_UID, 100, C.ORDEN_LOTE)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LOTE_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100, C.ORDEN_LOTE)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorLote.LOTE_AGREGADO, respuesta["mensaje"])

    def test_agregar_lote_correctamente_a_base_de_datos(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 234, C.ORDEN_LOTE)
        lote = self.__db.Lotes.buscar_por_uid(C.LOTE_UID)
        self.assertEqual(234, lote.obtener_precio_base())
        self.assertEqual(1, lote.obtener_orden())
        self.assertEqual(C.SUBASTA_UID, lote.obtener_subasta_uid())
        self.assertEqual(C.LOTE_UID, lote.obtener_uid())

    @data("", None, -1, 0)
    def test_retorna_error_obteniendo_subasta_invalida(self, subasta_invalida):
        sut = ControladorLote(self.__db)
        sut.obtener(subasta_invalida, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.BUSCAR_SIN_SUBASTA, respuesta["mensaje"])

    def test_retorna_error_obteniendo_subasta_inexistente(self):
        sut = ControladorLote(self.__db)
        sut.obtener(C.OTRA_SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_comienza_con_el_primer_lote_correctamente(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100, C.ORDEN_LOTE)
        sut.obtener(C.SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = ControladorLote(self.__db)
        self.__db.Articulos.crear(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO,
                                  self.__db.Usuarios.buscar_usuario_por_uid(1))
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100, C.ORDEN_LOTE)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 200, C.OTRO_ORDEN_LOTE)
        sut.obtener(C.SUBASTA_UID, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])

    def test_retorna_error_cuando_lote_no_existe_en_lista(self):
        consignatario = self.__db.Usuarios.buscar_usuario_por_uid(1)
        sut = ControladorLote(self.__db)
        self.__db.Articulos.crear(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, consignatario)
        self.__db.Articulos.crear(C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO,
                                  consignatario)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100, 1)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 200, 5)
        sut.obtener(C.SUBASTA_UID, 3)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LOTE_INEXISTENTE, respuesta["mensaje"])

    @data(-1, 1)
    def test_retorna_error_cuando_intenta_acceder_lote_invalido(self, orden: int):
        sut = ControladorLote(self.__db)
        sut.obtener(C.SUBASTA_UID, orden)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LOTE_INEXISTENTE, respuesta["mensaje"])

    @data(None, "", 0, -1)
    def test_retornar_error_listando_subasta_invalida(self, subasta_invalida):
        sut = ControladorLote(self.__db)
        sut.listar(subasta_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LISTAR_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_listando_subasta_inexistente(self):
        sut = ControladorLote(self.__db)
        sut.listar(C.OTRA_SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LISTAR_CON_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_vacio_cuando_subasta_no_tiene_lotes(self):
        sut = ControladorLote(self.__db)
        sut.listar(C.SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([], respuesta["items"])

    def test_retornar_catalogo_ordenado_cuando_subasta_tiene_lotes(self):
        consignatario = self.__db.Usuarios.buscar_usuario_por_uid(1)
        subasta = self.__db.Subastas.crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        articulo = self.__db.Articulos.crear(C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO,
                                             consignatario)
        self.__db.Lotes.agregar(subasta, articulo, C.BASE_LOTE, C.OTRO_ORDEN_LOTE)

        articulo = self.__db.Articulos.crear(C.OTRO_TITULO_ARTICULO, C.OTRA_DESCRIPCION_ARTICULO, C.OTRA_VALUACION_ARTICULO,
                                             consignatario)
        self.__db.Lotes.agregar(subasta, articulo, C.OTRA_BASE_LOTE, C.ORDEN_LOTE)
        sut = ControladorLote(self.__db)
        sut.listar(subasta.obtener_uid())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn({"articulo": {
            "id": 3,
            "consignatario_id": 1,
            "titulo": "Reloj de Arena",
            "descripcion": "Un reloj de arena que atrasa.",
            "valuacion": 3000}, "base": 5000, "orden": 1}, respuesta["items"])
        self.assertIn({"articulo": {
            "id": 2,
            "consignatario_id": 1,
            "titulo": "Sofa Antiguo",
            "descripcion": "Un sofa de principios de siglo.",
            "valuacion": 15000}, "base": 100, "orden": 2}, respuesta["items"])


if __name__ == "__main__":
    unittest.main()
