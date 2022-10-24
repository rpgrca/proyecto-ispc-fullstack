import unittest
import uuid
from ddt import ddt, data, unpack
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

    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasFake([], FakeGeneradorUid(SubastaControllerTests.SUBASTA_UID))) \
            .con_articulos(ArticulosFake([ Articulo(SubastaControllerTests.ARTICULO_UID) ])) \
            .construir()

    @data(
        ("", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000, "titulo"),
        (None, "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000, "titulo"),
        ("Subasta!", "", "gransubasta.jpg", 9/17/2000, "descripcion"),
        ("Subasta!", None, "gransubasta.jpg", 9/17/2000, "descripcion"),
        ("Subasta!", "Nos vemos en la subasta!", "", 9/17/2000, "imagen"),
        ("Subasta!", "Nos vemos en la subasta!", None, 9/17/2000, "imagen"),
        ("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", "", "fecha"),
        ("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", None, "fecha")
    )
    @unpack
    def test_retornar_error_cuando_falta_un_dato_en_creacion(self, titulo, descripcion, imagen, fecha, error):
        sut = SubastaController(self.__db)
        sut.crear(titulo, descripcion, imagen, fecha)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn("No se puede crear una subasta sin", respuesta["mensaje"])
        self.assertIn(error, respuesta["mensaje"])

    def test_crear_subasta_correctamente_cuando_datos_completos(self):
        sut = SubastaController(self.__db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 8/17/2000)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertIn("La subasta ha sido agendada para", respuesta["mensaje"])
        self.assertEqual(SubastaControllerTests.SUBASTA_UID_STR, respuesta["id"])

    def test_agrega_subasta_correctamente(self):
        lista = []
        db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasFake(lista)) \
            .construir()

        sut = SubastaController(db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 8/17/2000)
        self.assertEqual(1, len(lista))

    def test_retornar_error_cuando_falta_subasta_en_agregar(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(None, self._obtener_articulo_al_azar(), 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un lote sin subasta", respuesta["mensaje"])

    def _obtener_articulo_al_azar(self):
        return Articulo(uuid.uuid4())

    def test_retornar_error_cuando_falta_articulo_en_agregar(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, None, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un articulo nulo a una subasta", respuesta["mensaje"])

    def test_retornar_error_cuando_no_existe_articulo_para_agregar(self):
        sut = SubastaController(self.__db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 8/17/2000)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.OTRO_ARTICULO_UID_STR, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un articulo inexistente a una subasta", respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(SubastaControllerTests.OTRA_SUBASTA_UID_STR, self._obtener_articulo_al_azar(), 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un lote a una subasta inexistente", respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual("El lote ha sido agregado correctamente", respuesta["mensaje"])

    def test_comienza_con_el_primer_lote_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        sut.obtener_lote(SubastaControllerTests.SUBASTA_UID_STR, 1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(1, respuesta["item"]["orden"])

    def test_avanza_al_siguiente_lote_correctamente(self):
        sut = SubastaController(self.__db)
        self.__db.Articulos.agregar(uuid.UUID(SubastaControllerTests.OTRO_ARTICULO_UID_STR))
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.OTRO_ARTICULO_UID_STR, 200)
        sut.obtener_lote(SubastaControllerTests.SUBASTA_UID_STR, 2)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["item"]["orden"])
        
    def test_retorna_la_cantidad_de_lotes_correctamente(self):
        sut = SubastaController(self.__db)
        self.__db.Articulos.agregar(uuid.UUID(SubastaControllerTests.OTRO_ARTICULO_UID_STR))
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.ARTICULO_UID_STR, 100)
        sut.agregar_lote(SubastaControllerTests.SUBASTA_UID_STR, SubastaControllerTests.OTRO_ARTICULO_UID_STR, 200)
        sut.contar_lotes(SubastaControllerTests.SUBASTA_UID_STR)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(2, respuesta["total"])

    @data(-1, 1)
    def test_retorna_error_cuando_intenta_acceder_lote_invalido(self, orden: int):
        sut = SubastaController(self.__db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000)
        sut.obtener_lote(SubastaControllerTests.SUBASTA_UID_STR, orden)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No existe tal lote", respuesta["mensaje"])
   

if __name__ == "__main__":
    unittest.main()