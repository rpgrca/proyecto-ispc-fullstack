import unittest
import uuid
from ddt import ddt, data, unpack
from controller.subasta import SubastaController
from model.articulos import Articulo
from model.base_temporal import CreadorDeBasesDeDatosTemporales, SubastasFake
from model.generador_uid import FakeGeneradorUid
from model.lotes import Lote
from model.subastas import Subasta

@ddt
class SubastaControllerTests(unittest.TestCase):
    SUBASTA_UID = "57b212a8-4238-4acb-8932-4f8e06b85fd6"

    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_subastas(SubastasFake([], FakeGeneradorUid(uuid.UUID(SubastaControllerTests.SUBASTA_UID)))) \
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
        self.assertEqual(SubastaControllerTests.SUBASTA_UID, respuesta["id"])

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
        sut.agregar_lote(None, Lote(Articulo(), 100))
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un lote sin subasta", respuesta["mensaje"])

    def test_retornar_error_cuando_falta_lote_en_agregar(self):
        sut = SubastaController(self.__db)
        sut.agregar_lote(uuid.UUID(SubastaControllerTests.SUBASTA_UID), None)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un lote nulo a una subasta", respuesta["mensaje"])

    def test_retornar_error_cuando_subasta_no_se_encuentra(self):
        sut = SubastaController(self.__db)
        lote = Lote(Articulo(), 100)
        sut.agregar_lote(uuid.UUID("1a718eb8-8fa6-4c94-9a34-b933fad60776"), lote)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede agregar un lote a una subasta inexistente", respuesta["mensaje"])

    def test_agregar_lote_correctamente(self):
        sut = SubastaController(self.__db)
        sut.crear("Subasta!", "Nos vemos en la subasta!", "gransubasta.jpg", 9/17/2000)
        lote = Lote(Articulo(), 100)
        sut.agregar_lote(uuid.UUID(SubastaControllerTests.SUBASTA_UID), lote)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual("El lote ha sido agregado correctamente", respuesta["mensaje"])
       


if __name__ == "__main__":
    unittest.main()