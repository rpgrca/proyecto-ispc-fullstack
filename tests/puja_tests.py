import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.puja import ServicioPuja
from model.lotes import Lote
from model.articulos import Articulo
from model.subastas import Subasta
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import ArticulosEnMemoria, CreadorDeBasesDeDatosTemporales
from model.content_provider.memory import LotesEnMemoria, SubastasEnMemoria, UsuariosEnMemoria


@ddt
class ServicioPujaTests(unittest.TestCase):
    def setUp(self):
        subasta = Subasta(C.SUBASTA_UID, C.TITULO_SUBASTA, C.DESCRIPCION_SUBASTA, C.IMAGEN_SUBASTA, C.FECHA_DE_SUBASTA)
        articulo = Articulo(C.ARTICULO_UID)
        self.__db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria({C.NOMBRE_USUARIO: {
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

    @data("", None)
    def test_retornar_error_al_agregar_puja_con_lote_invalido(self, lote_invalido):
        sut = ServicioPuja(self.__db)
        sut.agregar(lote_invalido, C.ID_USUARIO, C.MONTO_PUJA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.PUJAR_SIN_LOTE, respuesta["mensaje"])

    @data("", None)
    def test_retornar_error_al_agregar_puja_con_pujador_invalido(self, pujador_invalido):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.LOTE_UID, pujador_invalido, C.MONTO_PUJA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.PUJAR_SIN_PUJADOR, respuesta["mensaje"])

    def test_retornar_error_al_agregar_puja_con_lote_inexistente(self):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.OTRO_LOTE_UID, C.ID_USUARIO, C.MONTO_PUJA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.LOTE_INEXISTENTE, respuesta["mensaje"])

    def test_retornar_error_al_agregar_puja_con_pujador_inexistente(self):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.LOTE_UID, C.OTRO_ID_USUARIO, C.MONTO_PUJA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.PUJADOR_INEXISTENTE, respuesta["mensaje"])

    @data(None, 0)
    def test_retornar_error_al_agregar_puja_con_monto_invalido(self, monto_invalido):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.LOTE_UID, C.ID_USUARIO, monto_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.MONTO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_al_agregar_puja_con_monto_invalido(self):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.LOTE_UID, C.ID_USUARIO, -1)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.MONTO_INVALIDO, respuesta["mensaje"])

    def test_retornar_error_al_agregar_puja_menor_a_anterior(self):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.LOTE_UID, C.ID_USUARIO, C.OTRO_MONTO_PUJA)
        sut.agregar(C.LOTE_UID, C.ID_USUARIO, C.MONTO_PUJA)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioPuja.PUJA_BAJA, respuesta["mensaje"])
       


    def test_agregar_puja_correctamente(self):
        sut = ServicioPuja(self.__db)
        sut.agregar(C.LOTE_UID, C.ID_USUARIO, C.MONTO_PUJA)
        puja = self.__db.Pujas.buscar_por_uid(C.PUJA_UID)
        self.assertEqual(C.LOTE_UID, puja.obtener_lote_uid())
        self.assertEqual(C.ID_USUARIO, puja.obtener_pujador_uid())
        self.assertEqual(C.MONTO_PUJA, puja.obtener_monto())


if __name__ == "__main__":
    unittest.main()
