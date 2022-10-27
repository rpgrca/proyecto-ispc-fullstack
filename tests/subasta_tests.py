import unittest
from ddt import ddt, data, unpack
from tests.constantes import *
from controller.subasta import SubastaController
from model.articulos import Articulo
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria


@ddt
class SubastaControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria([])) \
            .con_articulos(ArticulosEnMemoria([Articulo(ARTICULO_UID)])) \
            .construir()

    @data(
        ("", DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA, "titulo", SubastaController.SIN_TITULO),
        (None, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA, "titulo", SubastaController.SIN_TITULO),
        (TITULO_SUBASTA, "", IMAGEN_SUBASTA, FECHA_DE_SUBASTA, "descripcion", SubastaController.SIN_DESCRIPCION),
        (TITULO_SUBASTA, None, IMAGEN_SUBASTA, FECHA_DE_SUBASTA, "descripcion", SubastaController.SIN_DESCRIPCION),
        (TITULO_SUBASTA, DESCRIPCION_SUBASTA, "", FECHA_DE_SUBASTA, "imagen", SubastaController.SIN_IMAGEN),
        (TITULO_SUBASTA, DESCRIPCION_SUBASTA, None, FECHA_DE_SUBASTA, "imagen", SubastaController.SIN_IMAGEN),
        (TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, "", "fecha", SubastaController.SIN_FECHA),
        (TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, None, "fecha", SubastaController.SIN_FECHA)
    )
    @unpack
    def test_retornar_error_cuando_falta_un_dato_en_creacion(self, titulo, descripcion, imagen, fecha, error, mensaje_error):
        sut = SubastaController(self.__db)
        sut.crear(titulo, descripcion, imagen, fecha)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])
        self.assertIn(error, respuesta["mensaje"])

    def test_crear_subasta_correctamente_cuando_datos_completos(self):
        sut = SubastaController(self.__db)
        sut.crear(TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("La subasta ha sido agendada para", respuesta["mensaje"])
        self.assertEqual(SUBASTA_UID, respuesta["id"])

    def test_completar_datos_subasta_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear(TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA)
        subasta = self.__db.Subastas.buscar_por_uid(SUBASTA_UID)
        self.assertEqual(TITULO_SUBASTA, subasta.obtener_titulo())
        self.assertEqual(DESCRIPCION_SUBASTA, subasta.obtener_descripcion())
        self.assertEqual(IMAGEN_SUBASTA, subasta.obtener_imagen())
        self.assertEqual(FECHA_DE_SUBASTA, subasta.obtener_fecha())

    def test_agrega_subasta_correctamente(self):
        lista = []
        db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria(lista)) \
            .construir()

        sut = SubastaController(db)
        sut.crear(TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA)
        self.assertEqual(1, len(lista))


if __name__ == "__main__":
    unittest.main()

