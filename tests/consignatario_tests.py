import unittest
import tests.constantes as C
from controller.usuario import ControladorConsignatario
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


class ControladorConsignatarioTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_consignatario(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria(diccionario)) \
            .construir()

        sut = ControladorConsignatario(db)
        sut.agregar(C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO,
                    C.CLAVE_USUARIO, C.FECHA_NACIMIENTO_USUARIO)
        self.assertEqual(TipoDeUsuario.Consignatario.value, diccionario[C.NOMBRE_USUARIO]["tipo"])


if __name__ == "__main__":
    unittest.main()
