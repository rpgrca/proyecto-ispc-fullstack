import unittest
from ddt import ddt, data
from controller.lote import LoteController
from model.articulos import Articulo
from model.subastas import Subasta
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria


@ddt
class LoteControllerTests(unittest.TestCase):
    SUBASTA_UID = 1
    OTRA_SUBASTA_UID = 17
    ARTICULO_UID = 16
    OTRO_ARTICULO_UID = 20
    TITULO_SUBASTA = "Subasta!"
    DESCRIPCION_SUBASTA = "Nos vemos en la subasta!"
    IMAGEN_SUBASTA = "gransubasta.jpg"
    FECHA_DE_SUBASTA = 9/17/2000

    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria([Subasta(self.SUBASTA_UID, self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([Articulo(LoteControllerTests.ARTICULO_UID)])) \
            .construir()

    def test_retorna_la_cantidad_de_lotes_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(LoteControllerTests.SUBASTA_UID, LoteControllerTests.ARTICULO_UID, 100)
        sut.contar_lotes_en(LoteControllerTests.SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["total"])

    def test_retornar_error_cuando_falta_subasta_en_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(None, LoteControllerTests.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_falta_articulo_en_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(LoteControllerTests.SUBASTA_UID, None, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.ARTICULO_NULO_EN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(LoteControllerTests.SUBASTA_UID, LoteControllerTests.OTRO_ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = LoteController(self.__db)
        sut.agregar(LoteControllerTests.OTRA_SUBASTA_UID, LoteControllerTests.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(LoteControllerTests.SUBASTA_UID, LoteControllerTests.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(LoteController.LOTE_AGREGADO, respuesta["mensaje"])

    def test_comienza_con_el_primer_lote_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(LoteControllerTests.SUBASTA_UID, LoteControllerTests.ARTICULO_UID, 100)
        sut.obtener(LoteControllerTests.SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = LoteController(self.__db)
        self.__db.Articulos.agregar(LoteControllerTests.OTRO_ARTICULO_UID)
        sut.agregar(LoteControllerTests.SUBASTA_UID, LoteControllerTests.ARTICULO_UID, 100)
        sut.agregar(LoteControllerTests.SUBASTA_UID, LoteControllerTests.OTRO_ARTICULO_UID, 200)
        sut.obtener(LoteControllerTests.SUBASTA_UID, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])

    @data(-1, 1)
    def test_retorna_error_cuando_intenta_acceder_lote_invalido(self, orden: int):
        sut = LoteController(self.__db)
        sut.obtener(LoteControllerTests.SUBASTA_UID, orden)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_INEXISTENTE, respuesta["mensaje"])
