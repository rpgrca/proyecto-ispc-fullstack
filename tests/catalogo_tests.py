import unittest
from ddt import ddt, data
from services.lotes import ServicioLote
import tests.constantes as C
from controller.catalogo import ControladorCatalogo
from model.content_provider.memory import CreadorDeBasesDeDatosTemporales
from model.content_provider.memory import ArticulosEnMemoria


@ddt
class ControladorCatalogoTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_articulos(ArticulosEnMemoria([])) \
            .construir()

    @data(None, "", 0, -1)
    def test_retornar_error_listando_subasta_invalida(self, subasta_invalida):
        sut = ControladorCatalogo(self.__db)
        sut.listar(subasta_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LISTAR_SIN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_listando_subasta_inexistente(self):
        sut = ControladorCatalogo(self.__db)
        sut.listar(C.OTRA_SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLote.LISTAR_CON_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_vacio_cuando_subasta_no_tiene_lotes(self):
        sut = ControladorCatalogo(self.__db)
        sut.listar(C.SUBASTA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([], respuesta["items"])

    def test_retornar_catalogo_ordenado_cuando_subasta_tiene_lotes(self):
        subasta = self.__db.Subastas.crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        articulo = self.__db.Articulos.crear(C.ARTICULO_UID, C.TITULO_ARTICULO)
        self.__db.Lotes.agregar(subasta, articulo, C.BASE_LOTE, C.OTRO_ORDEN_LOTE)

        articulo = self.__db.Articulos.crear(C.OTRO_ARTICULO_UID, C.OTRO_TITULO_ARTICULO)
        self.__db.Lotes.agregar(subasta, articulo, C.OTRA_BASE_LOTE, C.ORDEN_LOTE)
        sut = ControladorCatalogo(self.__db)
        sut.listar(subasta.obtener_uid())
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn({"articulo": {"id": 20, "consignatario_id": 1, "titulo": "Reloj de Arena"}, "base": 5000, "orden": 1},
                      respuesta["items"])
        self.assertIn({"articulo": {"id": 16, "consignatario_id": 1, "titulo": "Sofa Antiguo"}, "base": 100, "orden": 2},
                      respuesta["items"])
