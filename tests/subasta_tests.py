import unittest
from ddt import ddt, data, unpack
from controller.subasta import SubastaController
from model.base_temporal import CreadorDeBasesDeDatosTemporales

@ddt
class SubastaControllerTests(unittest.TestCase):
    def setUp(self):
        self.__db = CreadorDeBasesDeDatosTemporales().construir()

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
    def test_retornar_error_cuando_falta_un_dato(self, titulo, descripcion, imagen, fecha, error):
        sut = SubastaController(self.__db)
        sut.crear(titulo, descripcion, imagen, fecha)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertIn("No se puede crear una subasta sin", respuesta["mensaje"])
        self.assertIn(error, respuesta["mensaje"])


if __name__ == "__main__":
    unittest.main()