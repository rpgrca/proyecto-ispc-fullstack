import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.libro_diario import ControladorLibroDiario
from model.articulos import Articulo
from model.lotes import Lote
from services.libro_diario import ServicioLibroDiario
from model.pujas import Puja
from model.subastas import Subasta
from model.usuarios import Usuario, UsuariosFactory
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import ArticulosEnMemoria, LotesEnMemoria, PujasEnMemoria, SubastasEnMemoria, UsuariosEnMemoria
from model.content_provider.memory import CreadorDeBasesDeDatosTemporales


@ddt
class ControladorVentaTests(unittest.TestCase):
    def setUp(self):
        articulo = Articulo(C.ARTICULO_UID, C.TITULO_ARTICULO)
        lote = Lote(C.LOTE_UID, C.SUBASTA_UID, articulo, C.BASE_LOTE, C.ORDEN_LOTE)
        pujador = UsuariosFactory.crear(C.ID_USUARIO, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.EMAIL_USUARIO, C.NOMBRE_USUARIO,
                                        C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)
        usuarios = UsuariosEnMemoria(self._list_to_dictionary([pujador]))

        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(usuarios) \
            .con_subastas(SubastasEnMemoria([Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA,
                                                     C.FECHA_DE_SUBASTA)])) \
            .con_articulos(ArticulosEnMemoria([articulo])) \
            .con_lotes(LotesEnMemoria([lote])) \
            .con_pujas(PujasEnMemoria([Puja(C.PUJA_UID, pujador, lote, C.MONTO_PUJA)])) \
            .construir()

    def _list_to_dictionary(self, usuarios: list[Usuario]):
        diccionario = {}
        for usuario in usuarios:
            diccionario[usuario.obtener_usuario()] = {
                "id": usuario.obtener_uid(),
                "nombre": usuario.obtener_nombre(),
                "apellido": usuario.obtener_apellido(),
                "email": usuario.obtener_email(),
                "usuario": usuario.obtener_usuario(),
                "clave": usuario.obtener_clave(),
                "nacimiento": usuario.obtener_nacimiento(),
                "tipo": usuario.obtener_tipo().value
            }

        return diccionario

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
        self.assertEqual(C.ID_USUARIO, venta.obtener_ganador().obtener_uid())
        self.assertEqual(1, venta.obtener_uid())
        self.assertEqual(C.TITULO_ARTICULO, venta.obtener_nombre_lote())
        self.assertEqual(485, venta.obtener_pago_a_consignatario())
        self.assertEqual(50, venta.obtener_precio_final())
        self.assertEqual(616, venta.obtener_comision())

    @data(None, "", -1, 0)
    def test_retornar_error_con_puja_invalida(self, puja_invalida):
        sut = ControladorLibroDiario(self.__db)
        sut.vender(puja_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLibroDiario.PUJA_INVALIDA, respuesta["mensaje"])

    def test_retornar_error_con_puja_inexistente(self):
        sut = ControladorLibroDiario(self.__db)
        sut.vender(C.OTRA_PUJA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLibroDiario.PUJA_INEXISTENTE, respuesta["mensaje"])

    @data(None, "", -1, 0)
    def test_retornar_error_listando_compras_de_pujador_invalido(self, pujador_invalido):
        sut = ControladorLibroDiario(self.__db)
        sut.listar_compras_de(pujador_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLibroDiario.PUJADOR_INVALIDO, respuesta["mensaje"])
 
    def test_retornar_error_listando_compras_de_pujador_inexistente(self):
        sut = ControladorLibroDiario(self.__db)
        sut.listar_compras_de(C.OTRO_ID_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLibroDiario.PUJADOR_INEXISTENTE, respuesta["mensaje"])
 
    def test_retornar_lista_vacia_con_pujador_sin_compra(self):
        sut = ControladorLibroDiario(self.__db)
        sut.listar_compras_de(C.ID_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([], respuesta["items"])
 
    def test_retornar_lista_con_compras_correctamente(self):
        sut = ControladorLibroDiario(self.__db)
        sut.vender(C.PUJA_UID)
        sut.listar_compras_de(C.ID_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([{"id": 1, "titulo": "Sofa Antiguo", "ganador": "Roberto", "precio": 50.0, "comision": 616.0,
                           "pago consignatario": 485.0}], respuesta["items"])
