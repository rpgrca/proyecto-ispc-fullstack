import unittest
import tests.constantes as C
from controller.registro import ServicioRegistro
from model.tipo_usuario import TipoDeUsuario
from model.content_provider.memory import UsuariosEnMemoria, CreadorDeBasesDeDatosTemporales


class ServicioRegistroTests(unittest.TestCase):
    def test_graba_usuario_de_tipo_pujador(self):
        diccionario = {}
        db = CreadorDeBasesDeDatosTemporales() \
            .con_usuarios(UsuariosEnMemoria(diccionario)) \
            .construir()

        ServicioRegistro(db, C.NOMBRE_USUARIO, C.APELLIDO_USUARIO, C.OTRO_EMAIL_USUARIO, C.NOMBRE_USUARIO, C.CLAVE_USUARIO,
                         C.FECHA_NACIMIENTO_USUARIO)
        self.assertEqual(TipoDeUsuario.Pujador.value, diccionario[C.NOMBRE_USUARIO]["tipo"])


if __name__ == "__main__":
    unittest.main()
