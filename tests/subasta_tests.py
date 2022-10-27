import unittest
from ddt import ddt, data, unpack
import tests.constantes as C
from controller.subasta import ServicioSubasta
from model.articulos import Articulo
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, SubastasEnMemoria


@ddt
class ServicioSubastaTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria([])) \
            .con_articulos(ArticulosEnMemoria([Articulo(C.ARTICULO_UID)])) \
            .construir()

    @data(
        ("", C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA, "titulo", ServicioSubasta.SIN_TITULO),
        (None, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA, "titulo", ServicioSubasta.SIN_TITULO),
        (C.TITULO_SUBASTA, "", C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA, "descripcion", ServicioSubasta.SIN_DESCRIPCION),
        (C.TITULO_SUBASTA, None, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA, "descripcion", ServicioSubasta.SIN_DESCRIPCION),
        (C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, "", C.FECHA_DE_SUBASTA, "imagen", ServicioSubasta.SIN_IMAGEN),
        (C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, None, C.FECHA_DE_SUBASTA, "imagen", ServicioSubasta.SIN_IMAGEN),
        (C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, "", "fecha", ServicioSubasta.SIN_FECHA),
        (C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, None, "fecha", ServicioSubasta.SIN_FECHA)
    )
    @unpack
    def test_retornar_error_cuando_falta_un_dato_en_creacion(self, titulo, descripcion, imagen, fecha, error, mensaje_error):
        sut = ServicioSubasta(self.__db)
        sut.crear(titulo, descripcion, imagen, fecha)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn(mensaje_error, respuesta["mensaje"])
        self.assertIn(error, respuesta["mensaje"])

    def test_crear_subasta_correctamente_cuando_datos_completos(self):
        sut = ServicioSubasta(self.__db)
        sut.crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("La subasta ha sido agendada para", respuesta["mensaje"])
        self.assertEqual(C.SUBASTA_UID, respuesta["id"])

    def test_completar_datos_subasta_correctamente(self):
        sut = ServicioSubasta(self.__db)
        sut.crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        subasta = self.__db.Subastas.buscar_por_uid(C.SUBASTA_UID)
        self.assertEqual(C.TITULO_SUBASTA, subasta.obtener_titulo())
        self.assertEqual(C.DESCRIPCION_SUBASTA, subasta.obtener_descripcion())
        self.assertEqual(C.IMAGEN_SUBASTA, subasta.obtener_imagen())
        self.assertEqual(C.FECHA_DE_SUBASTA, subasta.obtener_fecha())

    def test_agrega_subasta_correctamente(self):
        lista = []
        db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasEnMemoria(lista)) \
            .construir()

        sut = ServicioSubasta(db)
        sut.crear(C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        self.assertEqual(1, len(lista))


if __name__ == "__main__":
    unittest.main()
