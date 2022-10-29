import unittest
from tests.articulo_tests import ControladorArticuloTests
from tests.lote_tests import ControladorLoteTests
from tests.puja_tests import ControladorPujaTests
from tests.pujador_tests import ServicioPujadorTests
from tests.consignatario_tests import ControladorConsignatarioTests
from tests.login_tests import ServicioLoginTests
from tests.registro_tests import ControladorRegistroTests
from tests.reestablecer_tests import ServicioReestablecerTests
from tests.usuario_tests import ControladorUsuarioTests
from tests.subasta_tests import ControladorSubastaTests
from tests.venta_tests import ControladorVentaTests
from tests.catalogo_tests import ControladorCatalogoTests

suite = unittest.TestSuite()

suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioLoginTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorUsuarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorRegistroTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioReestablecerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioPujadorTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorConsignatarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorSubastaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorLoteTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorPujaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorArticuloTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorVentaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorCatalogoTests))

unittest.TextTestRunner(verbosity=3).run(suite)
