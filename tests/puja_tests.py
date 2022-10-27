import unittest
from ddt import ddt
import tests.constantes as C
from controller.puja import PujaController
from model.lotes import Lote
from model.articulos import Articulo
from model.subastas import Subasta
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales, LotesEnMemoria, SubastasEnMemoria, UsuariosEnMemoria


@ddt
class PujaControllerTests(unittest.TestCase):
    def setUp(self):
        subasta = Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        articulo = Articulo(C.ARTICULO_UID)
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({ C.NOMBRE_USUARIO: {
                "id": C.ID_USUARIO,
                "nombre": C.NOMBRE_USUARIO,
                "apellido": C.APELLIDO_USUARIO,
                "email": C.EMAIL_USUARIO,
                "usuario": C.NOMBRE_USUARIO,
                "clave": C.CLAVE_USUARIO,
                "nacimiento": C.FECHA_NACIMIENTO_USUARIO,
                "tipo": TipoDeUsuario.Pujador.value
            }})) \
            .con_subastas(SubastasEnMemoria([subasta])) \
            .con_lotes(LotesEnMemoria([Lote(C.LOTE_UID, subasta, articulo, C.BASE_LOTE, C.ORDEN_LOTE)])) \
            .con_articulos(ArticulosEnMemoria([articulo])) \
            .construir()

    def test_crear_puja_correctamente(self):
        sut = PujaController(self.__db)
        sut.agregar(C.LOTE_UID, C.ID_USUARIO, C.MONTO_PUJA)
        puja = self.__db.Pujas.buscar_por_uid(C.PUJA_UID)
        self.assertEqual(C.LOTE_UID, puja.obtener_lote_uid())
        self.assertEqual(C.ID_USUARIO, puja.obtener_pujador_uid())
        self.assertEqual(C.MONTO_PUJA, puja.obtener_monto())


if __name__ == "__main__":
    unittest.main()
