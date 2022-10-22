import unittest
from tests.login_tests import LoginControllerTests

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.makeSuite(LoginControllerTests))
    
    unittest.TextTestRunner(verbosity=3).run(suite)