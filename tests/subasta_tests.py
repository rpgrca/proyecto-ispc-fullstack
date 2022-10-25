import unittest
import uuid
from ddt import ddt, data, unpack
from controller.controller import Controller
from controller.subasta import SubastaController
from model.articulos import Articulo
from model.base_temporal import ArticulosFake, CreadorDeBasesDeDatosTemporales, SubastasFake
from model.generador_uid import FakeGeneradorUid

@ddt
class SubastaControllerTests(unittest.TestCase):
    SUBASTA_UID_STR = "57b212a8-4238-4acb-8932-4f8e06b85fd6"
    SUBASTA_UID = uuid.UUID(SUBASTA_UID_STR)
    OTRA_SUBASTA_UID_STR = "1a718eb8-8fa6-4c94-9a34-b933fad60776"
    ARTICULO_UID_STR = "3d1d675e-232a-4468-9f40-4d63d91c49aa"
    ARTICULO_UID = uuid.UUID(ARTICULO_UID_STR)
    OTRO_ARTICULO_UID_STR = "5bd58a25-81b3-4b79-b07f-d6a3812df7e8"
    TITULO_SUBASTA = "Subasta!"
    DESCRIPCION_SUBASTA = "Nos vemos en la subasta!"
    IMAGEN_SUBASTA = "gransubasta.jpg"
    FECHA_DE_SUBASTA = 9/17/2000

    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasFake([], FakeGeneradorUid(SubastaControllerTests.SUBASTA_UID))) \
            .con_articulos(ArticulosFake([ Articulo(SubastaControllerTests.ARTICULO_UID) ])) \
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
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("La subasta ha sido agendada para", respuesta["mensaje"])
        self.assertEqual(SubastaControllerTests.SUBASTA_UID_STR, respuesta["id"])

    def test_completar_datos_subasta_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        subasta = self.__db.Subastas.buscar_por_uid(SubastaControllerTests.SUBASTA_UID)
        self.assertEqual(self.TITULO_SUBASTA, subasta.obtener_titulo())
        self.assertEqual(self.DESCRIPCION_SUBASTA, subasta.obtener_descripcion())
        self.assertEqual(self.IMAGEN_SUBASTA, subasta.obtener_imagen())
        self.assertEqual(self.FECHA_DE_SUBASTA, subasta.obtener_fecha())

    def test_agrega_subasta_correctamente(self):
        lista = []
        db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasFake(lista)) \
            .construir()

        sut = SubastaController(db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        self.assertEqual(1, len(lista))

    def test_retornar_error_cuando_falta_subasta_en_agregar(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(None, SubastaControllerTests.ARTICULO_UID_STR, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(SubastaController.LOTE_SIN_SUBASTA, respuesta["mensaje"])

    @data(
        ("uuid invalido", ARTICULO_UID_STR),
        (SUBASTA_UID_STR, "uuid invalido")
    )
    @unpack
    def test_retornar_error_cuando_uuid_invalido(self, subasta_uid, articulo_uid):
        sut = SubastaController(self.__db)
        sut.agregar_lote(subasta_uid, articulo_uid, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(Controller.UUID_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_cuando_falta_articulo_en_agregar(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, None, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(SubastaController.ARTICULO_NULO_EN_SUBASTA, respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.OTRO_ARTICULO_UID_STR, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(SubastaController.ARTICULO_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(SubastaControllerTests.OTRA_SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(SubastaController.LOTE_SUBASTA_INEXISTENTE, respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(SubastaController.LOTE_AGREGADO, respuesta["mensaje"])

    def test_retornar_error_cuando_uuid_invalido_en_obtener(self):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.obtener_lote("uuid invalido", 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(Controller.UUID_INVALIDO, respuesta["mensaje"])

    def test_comienza_con_el_primer_lote_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        sut.obtener_lote(SubastaControllerTests.SUBASTA_UID_STR, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = SubastaController(self.__db)
        self.__db.Articulos.agregar(uuid.UUID(SubastaControllerTests.OTRO_ARTICULO_UID_STR))
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.OTRO_ARTICULO_UID_STR, 200)
        sut.obtener_lote(SubastaControllerTests.SUBASTA_UID_STR, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])
 
    def test_retornar_error_cuando_cuenta_lotes_de_uuid_invalido(self):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.contar_lotes("uuid invalido")
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(Controller.UUID_INVALIDO, respuesta["mensaje"])
        
    def test_retorna_la_cantidad_de_lotes_correctamente(self):
        sut = SubastaController(self.__db)
        self.__db.Articulos.agregar(uuid.UUID(SubastaControllerTests.OTRO_ARTICULO_UID_STR))
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.OTRO_ARTICULO_UID_STR, 200)
        sut.contar_lotes(SubastaControllerTests.SUBASTA_UID_STR)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["total"])

    @data(-1, 1)
    def test_retorna_error_cuando_intenta_acceder_lote_invalido(self, orden: int):
        sut = SubastaController(self.__db)
        sut.crear(self.TITULO_SUBASTA, self.DESCRIPCION_SUBASTA, self.IMAGEN_SUBASTA, self.FECHA_DE_SUBASTA)
        sut.obtener_lote(SubastaControllerTests.SUBASTA_UID_STR, orden)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(SubastaController.LOTE_INEXISTENTE, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()