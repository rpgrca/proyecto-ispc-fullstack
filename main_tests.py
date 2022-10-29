import unittest
from tests.lote_tests import ControladorLoteTests
from tests.puja_tests import ControladorPujaTests
from tests.pujador_tests import ServicioPujadorTests
from tests.consignatario_tests import ServicioConsignatarioTests
from tests.login_tests import ServicioLoginTests
from tests.registro_tests import ServicioRegistroTests
from tests.reestablecer_tests import ServicioReestablecerTests
from tests.usuario_tests import ControladorUsuarioTests
from tests.subasta_tests import ServicioSubastaTests

suite = unittest.TestSuite()

suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioLoginTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorUsuarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioRegistroTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioReestablecerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioPujadorTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioConsignatarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioSubastaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorLoteTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ControladorPujaTests))

unittest.TextTestRunner(verbosity=3).run(suite)
