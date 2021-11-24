import unittest
from unittest.mock import Mock, MagicMock, call, patch, PropertyMock
import app

class test_app(unittest.Testcase):
    def test_find_text_enclosed_inside(self):
        test_find = find_text_enclosed_inside('#test', '#')
        self.assertEqual('test', test_find)

def main():
    # Create a test suit
    suit = unittest.TestLoader().loadTestsFromTestCase(test_app)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
