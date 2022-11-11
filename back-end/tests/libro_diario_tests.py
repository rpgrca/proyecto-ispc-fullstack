import unittest
from ddt import ddt, data
import tests.constantes as C
from controller.libro_diario import ControladorLibroDiario
from model.articulos import Articulo
from model.lotes import Lote
from services.libro_diario import ServicioLibroDiario
from model.pujas import Puja
from model.subastas import Subasta
from model.usuarios import Usuario, Usuarios
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import ArticulosEnMemoria, LotesEnMemoria, PujasEnMemoria, SubastasEnMemoria
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


@ddt
class ControladorLibroDiarioTests(unittest.TestCase):
    def setUp(self):
        pujador = Usuarios.crear(C.ID_USUARIO, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.EMAIL_USUARIO, C.NOMBRE_USUARIO,
                                 C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Pujador)
        consignatario = Usuarios.crear(C.OTRO_ID_USUARIO, C.OTRO_NOMBRE_USUARIO, C.APELLIDO_USUARIO,
                                       C.OTRO_EMAIL_USUARIO, C.OTRO_NOMBRE_USUARIO, C.OTRA_CLAVE_USUARIO,
                                       C.FECHA_NACIMIENTO_USUARIO, TipoDeUsuario.Consignatario)
        usuarios = UsuariosEnMemoria(self._list_to_dictionary([pujador, consignatario]))
        articulo = Articulo(C.ARTICULO_UID, C.TITULO_ARTICULO, C.DESCRIPCION_ARTICULO, C.VALUACION_ARTICULO, consignatario)
        lote = Lote(C.LOTE_UID, C.SUBASTA_UID, articulo, C.BASE_LOTE, C.ORDEN_LOTE)

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
                "tipo": usuario.obtener_tipo()
            }

        return diccionario

    def test_retornar_ok_con_venta_exitosa(self):
        sut = ControladorLibroDiario(self.__db)
        sut.convertir_en_venta(C.PUJA_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(ControladorLibroDiario.VENTA_EXITOSA, respuesta["mensaje"])

    def test_crear_subasta_con_datos_correctos(self):
        sut = ControladorLibroDiario(self.__db)
        sut.convertir_en_venta(C.PUJA_UID)
        venta = self.__db.Ventas.buscar_por_uid(1)
        self.assertEqual(C.ID_USUARIO, venta.obtener_ganador().obtener_uid())
        self.assertEqual(1, venta.obtener_uid())
        self.assertEqual(C.TITULO_ARTICULO, venta.obtener_titulo_lote())
        self.assertEqual(485, venta.obtener_pago_a_consignatario())
        self.assertEqual(616, venta.obtener_precio_final())
        self.assertEqual(50, venta.obtener_comision())

    @data(None, "", -1, 0)
    def test_retornar_error_con_puja_invalida(self, puja_invalida):
        sut = ControladorLibroDiario(self.__db)
        sut.convertir_en_venta(puja_invalida)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual(ServicioLibroDiario.PUJA_INVALIDA, respuesta["mensaje"])

    def test_retornar_error_con_puja_inexistente(self):
        sut = ControladorLibroDiario(self.__db)
        sut.convertir_en_venta(C.OTRA_PUJA_UID)
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
        sut.convertir_en_venta(C.PUJA_UID)
        sut.listar_compras_de(C.ID_USUARIO)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual([{"id": 1, "titulo": "Sofa Antiguo", "ganador": "Roberto", "precio": 616.0, "comision": 50.0,
                           "pago consignatario": 485.0}], respuesta["items"])

    @data(None, "", -1)
    def test_retornar_error_al_cerrar_lote_invalido(self, lote_invalido):
        sut = ControladorLibroDiario(self.__db)
        sut.registrar_venta_en(lote_invalido)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede cerrar un lote inválido", respuesta["mensaje"])

    def test_retornar_error_al_cerrar_lote_inexistente(self):
        sut = ControladorLibroDiario(self.__db)
        sut.registrar_venta_en(100)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("error", respuesta["status"])
        self.assertEqual("No se puede cerrar un lote inexistente", respuesta["mensaje"])

    def test_retornar_ok_al_cerrar_lote_sin_pujas(self):
        db = CreadorDeBasesDeDatosTemporales() \
            .con_articulos(self.__db.Articulos) \
            .con_lotes(self.__db.Lotes) \
            .con_subastas(self.__db.Subastas) \
            .con_usuarios(self.__db.Usuarios) \
            .construir()

        sut = ControladorLibroDiario(db)
        sut.registrar_venta_en(C.LOTE_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual("El lote ha quedado desierto", respuesta["mensaje"])

    def test_retornar_ok_al_cerrar_lote_con_pujas(self):
        sut = ControladorLibroDiario(self.__db)
        sut.registrar_venta_en(C.LOTE_UID)
        respuesta = sut.obtener_respuesta()
        self.assertEqual("ok", respuesta["status"])
        self.assertEqual(616, respuesta["precio_final"])


if __name__ == "__main__":
    unittest.main()
