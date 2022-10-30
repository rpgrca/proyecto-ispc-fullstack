import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.lote import ControladorLote, ServicioLote
from model.articulos import Articulo
from model.subastas import Subasta
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria


@ddt
class ControladorLoteTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria([Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                     C.FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([Articulo(1, C.TITULO_ARTICULO)])) \
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
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        sut.contar_lotes_en(C.SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["total"])

    @data("", None, -1, 0)
    def test_retornar_error_cuando_falta_subasta_en_agregar(self, lote_invalido):
        sut = ControladorLote(self.__db)
        sut.agregar(lote_invalido, C.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LOTE_SIN_SUBASTA, respuesta["mensaje"])

    @data("", None, -1, 0)
    def test_retornar_error_cuando_falta_articulo_en_agregar(self, articulo_invalido):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, articulo_invalido, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.ARTICULO_NULO_EN_SUBASTA, respuesta["mensaje"])

    @data("", None, -1)
    def test_retornar_error_cuando_base_es_invalida(self, base_invalida):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, base_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.BASE_INVALIDA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.OTRA_SUBASTA_UID, C.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LOTE_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorLote.LOTE_AGREGADO, respuesta["mensaje"])

    def test_agregar_lote_correctamente_a_base_de_datos(self):
        sut = ControladorLote(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 234)
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
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        sut.obtener(C.SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = ControladorLote(self.__db)
        self.__db.Articulos.crear(C.TITULO_ARTICULO)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 200)
        sut.obtener(C.SUBASTA_UID, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])

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
        subasta = self.__db.Subastas.crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        articulo = self.__db.Articulos.crear(C.TITULO_ARTICULO)
        self.__db.Lotes.agregar(subasta, articulo, C.BASE_LOTE, C.OTRO_ORDEN_LOTE)

        articulo = self.__db.Articulos.crear(C.OTRO_TITULO_ARTICULO)
        self.__db.Lotes.agregar(subasta, articulo, C.OTRA_BASE_LOTE, C.ORDEN_LOTE)
        sut = ControladorLote(self.__db)
        sut.listar(subasta.obtener_uid())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn({"articulo": {"id": 3, "consignatario_id": 1, "titulo": "Reloj de Arena"}, "base": 5000, "orden": 1},
                      respuesta["items"])
        self.assertIn({"articulo": {"id": 2, "consignatario_id": 1, "titulo": "Sofa Antiguo"}, "base": 100, "orden": 2},
                      respuesta["items"])


if __name__ == "__main__":
    unittest.main()
