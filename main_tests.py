import unittest
from tests.lote_tests import ServicioLoteTests
from tests.puja_tests import ServicioPujaTests
from tests.pujador_tests import ServicioPujadorTests
from tests.consignatario_tests import ServicioConsignatarioTests
from tests.login_tests import ServicioLoginTests
from tests.registro_tests import ServicioRegistroTests
from tests.reestablecer_tests import ServicioReestablecerTests
from tests.usuario_tests import ServicioUsuarioTests
from tests.subasta_tests import ServicioSubastaTests

suite = unittest.TestSuite()

suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioLoginTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioUsuarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioRegistroTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioReestablecerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioPujadorTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioConsignatarioTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioSubastaTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioLoteTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ServicioPujaTests))

unittest.TextTestRunner(verbosity=3).run(suite)
