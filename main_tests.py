import unittest
from tests.login_tests import LoginControllerTests
from tests.registro_tests import RegistroControllerTests
from tests.reestablecer_tests import ReestablecerControllerTests

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.makeSuite(LoginControllerTests))
    suite.addTest(unittest.makeSuite(RegistroControllerTests))
    suite.addTest(unittest.makeSuite(ReestablecerControllerTests))
    
    unittest.TextTestRunner(verbosity=3).run(suite)