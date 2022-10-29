import unittest
from ddt import ddt
from controller.libro_diario import ControladorLibroDiario
from model.articulos import Articulo
from model.lotes import Lote
from model.pujas import Puja
from model.subastas import Subasta
from model.usuarios import UsuariosFactory
import tests.constantes as C
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import ArticulosEnMemoria, LotesEnMemoria, PujasEnMemoria, SubastasEnMemoria
from model.content_provider.memory import UsuariosCreadosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class ControladorVentaTests(unittest.TestCase):
    def setUp(self):
        articulo = Articulo(C.ARTICULO_UID, C.TITULO_ARTICULO)
        lote = Lote(C.LOTE_UID, C.SUBASTA_UID, articulo, C.BASE_LOTE, C.ORDEN_LOTE)
        pujador = UsuariosFactory.crear(C.ID_USUARIO, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.EMAIL_USUARIO, C.NOMBRE_USUARIO,
                                        C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)

        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosCreadosEnMemoria([pujador])) \
            .con_subastas(SubastasEnMemoria([Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                     C.FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([articulo])) \
            .con_lotes(LotesEnMemoria([lote])) \
            .con_pujas(PujasEnMemoria([Puja(C.PUJA_UID, pujador, lote, C.MONTO_PUJA)])) \
            .construir()

    def test_retornar_ok_con_venta_exitosa(self):
        sut = ControladorLibroDiario(self.__db)
        sut.vender(C.PUJA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorLibroDiario.VENTA_EXITOSA, respuesta["mensaje"])

    def test_crear_subasta_con_datos_correctos(self):
        sut = ControladorLibroDiario(self.__db)
        sut.vender(C.PUJA_UID)
        venta = self.__db.Ventas.buscar_por_uid(1)
        self.assertEqual(C.NOMBRE_USUARIO, venta.obtener_nombre_ganador())
        self.assertEqual(1, venta.obtener_uid())
        self.assertEqual(C.TITULO_ARTICULO, venta.obtener_nombre_lote())
        self.assertEqual(485, venta.obtener_pago_a_consignatario())
        self.assertEqual(50, venta.obtener_precio_final())
        self.assertAlmostEqual(616, venta.obtener_comision())
