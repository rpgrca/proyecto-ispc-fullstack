import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.lote import LoteController
from model.articulos import Articulo
from model.subastas import Subasta
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria


@ddt
class LoteControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria([Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                     C.FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([Articulo(C.ARTICULO_UID)])) \
            .construir()

    @data("", None)
    def test_retornar_error_cuando_la_subasta_es_invalida(self, subasta_invalida):
        sut = LoteController(self.__db)
        sut.contar_lotes_en(subasta_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.CONTAR_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_subasta(self):
        sut = LoteController(self.__db)
        sut.contar_lotes_en(C.OTRA_SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.CONTAR_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_retorna_la_cantidad_de_lotes_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        sut.contar_lotes_en(C.SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["total"])

    def test_retornar_error_cuando_falta_subasta_en_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(None, C.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_falta_articulo_en_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(C.SUBASTA_UID, None, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.ARTICULO_NULO_EN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = LoteController(self.__db)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = LoteController(self.__db)
        sut.agregar(C.OTRA_SUBASTA_UID, C.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(LoteController.LOTE_AGREGADO, respuesta["mensaje"])

    @data("", None)
    def test_retorna_error_con_subasta_invalida(self, subasta_invalida):
        sut = LoteController(self.__db)
        sut.obtener(subasta_invalida, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.BUSCAR_SIN_SUBASTA, respuesta["mensaje"])

    def test_retorna_error_con_subasta_inexistente(self):
        sut = LoteController(self.__db)
        sut.obtener(C.OTRA_SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_comienza_con_el_primer_lote_correctamente(self):
        sut = LoteController(self.__db)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        sut.obtener(C.SUBASTA_UID, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = LoteController(self.__db)
        self.__db.Articulos.agregar(C.OTRO_ARTICULO_UID)
        sut.agregar(C.SUBASTA_UID, C.ARTICULO_UID, 100)
        sut.agregar(C.SUBASTA_UID, C.OTRO_ARTICULO_UID, 200)
        sut.obtener(C.SUBASTA_UID, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])

    @data(-1, 1)
    def test_retorna_error_cuando_intenta_acceder_lote_invalido(self, orden: int):
        sut = LoteController(self.__db)
        sut.obtener(C.SUBASTA_UID, orden)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(LoteController.LOTE_INEXISTENTE, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()
