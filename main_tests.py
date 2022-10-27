import unittest
from tests.lote_tests import LoteControllerTests
from tests.pujador_tests import PujadorControllerTests
from tests.consignatario_tests import ConsignatarioControllerTests
from tests.login_tests import LoginControllerTests
from tests.registro_tests import RegistroControllerTests
from tests.reestablecer_tests import ReestablecerControllerTests
from tests.usuario_tests import UsuarioControllerTests
from tests.subasta_tests import SubastaControllerTests

suite = unittest.TestSuite()

suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoginControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(UsuarioControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RegistroControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ReestablecerControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PujadorControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ConsignatarioControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SubastaControllerTests))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoteControllerTests))

unittest.TextTestRunner(verbosity=3).run(suite)
