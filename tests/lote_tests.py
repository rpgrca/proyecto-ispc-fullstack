import unittest
from ddt import ddt, data
from tests.constantes import *
from controller.lote import LoteController
from model.articulos import Articulo
from model.subastas import Subasta
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria


@ddt
class LoteControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria([Subasta(SUBASTA_UID, TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([Articulo(ARTICULO_UID)])) \
            .construir()

    def test_retorna_la_cantidad_de_lotes_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(SUBASTA_UID, ARTICULO_UID, 100)
        sut.contar_lotes_en(SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["total"])

    def test_retornar_error_cuando_falta_subasta_en_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(None, ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_falta_articulo_en_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(SUBASTA_UID, None, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.ARTICULO_NULO_EN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(SUBASTA_UID, OTRO_ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = LoteController(self.__db)
        sut.agregar(OTRA_SUBASTA_UID, ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(SUBASTA_UID, ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(LoteController.LOTE_AGREGADO, respuesta["mensaje"])

    def test_comienza_con_el_primer_lote_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(SUBASTA_UID, ARTICULO_UID, 100)
        sut.obtener(SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = LoteController(self.__db)
        self.__db.Articulos.agregar(OTRO_ARTICULO_UID)
        sut.agregar(SUBASTA_UID, ARTICULO_UID, 100)
        sut.agregar(SUBASTA_UID, OTRO_ARTICULO_UID, 200)
        sut.obtener(SUBASTA_UID, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])

    @data(-1, 1)
    def test_retorna_error_cuando_intenta_acceder_lote_invalido(self, orden: int):
        sut = LoteController(self.__db)
        sut.obtener(SUBASTA_UID, orden)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_INEXISTENTE, respuesta["mensaje"])
