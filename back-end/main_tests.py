import unittest
from tests.articulo_tests import ControladorArticuloTests
from tests.lote_tests import ControladorLoteTests
from tests.puja_tests import ControladorPujaTests
from tests.login_tests import ServicioLoginTests
from tests.usuario_tests import ControladorUsuarioTests
from tests.subasta_tests import ControladorSubastaTests
from tests.libro_diario_tests import ControladorLibroDiarioTests

suite = unittest.TestSuite()

suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioLoginTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorUsuarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorSubastaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorLoteTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorPujaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorArticuloTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorLibroDiarioTests))

unittest.TextTestRunner(verbosity=3).run(suite)
