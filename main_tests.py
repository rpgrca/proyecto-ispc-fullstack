import unittest
from tests.pujador_tests import PujadorControllerTests
from tests.consignatario_tests import ConsignatarioControllerTests
from tests.login_tests import LoginControllerTests
from tests.registro_tests import RegistroControllerTests
from tests.reestablecer_tests import ReestablecerControllerTests
from tests.usuario_tests import UsuarioControllerTests
from tests.subasta_tests import SubastaControllerTests

suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(LoginControllerTests))
suite.addTest(unittest.makeSuite(UsuarioControllerTests))
suite.addTest(unittest.makeSuite(RegistroControllerTests))
suite.addTest(unittest.makeSuite(ReestablecerControllerTests))
suite.addTest(unittest.makeSuite(PujadorControllerTests))
suite.addTest(unittest.makeSuite(ConsignatarioControllerTests))
suite.addTest(unittest.makeSuite(SubastaControllerTests))

unittest.TextTestRunner(verbosity=3).run(suite)