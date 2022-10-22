import unittest
from tests.login_tests import LoginControllerTests
from tests.registro_tests import RegistroControllerTests

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.makeSuite(LoginControllerTests))
    suite.addTest(unittest.makeSuite(RegistroControllerTests))
    
    unittest.TextTestRunner(verbosity=3).run(suite)