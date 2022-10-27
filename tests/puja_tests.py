import unittest
from ddt import ddt, data
from tests.constantes import *
from controller.puja import PujaController
from model.lotes import Lote
from model.articulos import Articulo
from model.subastas import Subasta
from model.pujas import Puja
from model.usuarios import Pujador
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, LotesEnMemoria, SubastasEnMemoria, UsuariosEnMemoria


@ddt
class PujaControllerTests(unittest.TestCase):
    def setUp(self):
        subasta = Subasta(SUBASTA_UID, TITULO_SUBASTA, DESCRIPCION_SUBASTA, IMAGEN_SUBASTA, FECHA_DE_SUBASTA)
        articulo = Articulo(ARTICULO_UID)
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({ NOMBRE_USUARIO: {
                "id": ID_USUARIO,
                "nombre": NOMBRE_USUARIO,
                "apellido": APELLIDO_USUARIO,
                "email": EMAIL_USUARIO,
                "usuario": NOMBRE_USUARIO,
                "clave": CLAVE_USUARIO,
                "nacimiento": FECHA_NACIMIENTO_USUARIO,
                "tipo": TipoDeUsuario.Pujador.value
            }})) \
            .con_subastas(SubastasEnMemoria([subasta])) \
            .con_lotes(LotesEnMemoria([Lote(LOTE_UID, subasta, articulo, BASE_LOTE, ORDEN_LOTE)])) \
            .con_articulos(ArticulosEnMemoria([articulo])) \
            .construir()

    def test_crear_puja_correctamente(self):
        sut = PujaController(self.__db)
        sut.agregar(LOTE_UID, ID_USUARIO, MONTO_PUJA)
        subasta = self.__db.Subastas.buscar_por_uid(SUBASTA_UID)
        self.assertEqual(TITULO_SUBASTA, subasta.obtener_titulo())
        self.assertEqual(DESCRIPCION_SUBASTA, subasta.obtener_descripcion())
        self.assertEqual(IMAGEN_SUBASTA, subasta.obtener_imagen())
        self.assertEqual(FECHA_DE_SUBASTA, subasta.obtener_fecha())

    def agregar(self, monto: int, pujador: Pujador, lote: Lote):
        self.__pujas.append(Puja(monto, pujador, lote))


if __name__ == "__main__":
    unittest.main()

