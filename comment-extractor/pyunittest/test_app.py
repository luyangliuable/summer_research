import os
import sys
import inspect
import unittest
from unittest.mock import Mock, MagicMock, call, patch, PropertyMock
# relative imports from parent directory ######################################
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
# relative import ends ########################################################
import app

class test_app(unittest.TestCase):
    def test_find_text_enclosed_inside(self):
        test_find = app.find_text_enclosed_inside('#test', '#')
        self.assertEqual('test', test_find)

    def test_check_if_comment_is_empty_multi_line(self):
        test_check_python = app.check_if_comment_is_empty({'line': '""""""', 'location': '' }, app.python_comment)
        test_check_c = app.check_if_comment_is_empty({'line': '/* */', 'location': '' }, app.c_comment)
        test_false_c = app.check_if_comment_is_empty({'line': '/* has comment */', 'location': '' }, app.c_comment)
        self.assertTrue(test_check_python)
        self.assertTrue(test_check_c)
        self.assertFalse(test_false_c)

    # @unittest.skip('come back after all unittest is done')
    def test_check_if_comment_is_empty_single_line(self):
        test_check_python = app.check_if_comment_is_empty({'line': '', 'location': '' }, app.python_comment)
        test_false_python = app.check_if_comment_is_empty({'line': 'has comment', 'location': '' }, app.c_comment)
        test_check_c = app.check_if_comment_is_empty({'line': '//', 'location': '' }, app.c_comment)
        self.assertFalse(test_false_python)
        self.assertTrue(test_check_python)
        self.assertTrue(test_check_c)

    def test_check_file_is_same_format(self):
        filename = "a.testformat"
        test_format = app.check_file_is_same_format(filename, '*.testformat')
        test_format_false = app.check_file_is_same_format(filename, '*.randomformat')
        self.assertTrue(test_format)
        self.assertFalse(test_format_false)


    # @patch.object(TextIOWrapper, 'readline')
    def test_get_every_line_from_file(self):
        # result = MagicMock()
        # result.return_value = '""""multi line comment""""'
        # mock = result
        test_case = app.get_every_line_from_file('./test-folder/a.py')
        self.assertEqual(test_case[0]["line"], '"""')
        self.assertEqual(test_case[1]["line"], "multi line comment")

    def test_strip_comment_of_symbols(self):
        test_case = app.strip_comment_of_symbols('/* adasd', app.c_comment)
        self.assertEqual(test_case, ' adasd')

    def test_remove_starting_whitespace(self):
        test_case = app.remove_starting_whitespace("   test")
        self.assertEqual(test_case, "test")

    def test_extract_comment_from_line_list(self):
        line_list = [{'line': '"""', 'location': 'random' }, {'line': "line1", 'location': 'random'}, {'line': "line2", 'location': 'random'}, {'line': '"""', 'location': 'random'}, {'line': "line3", 'location': 'random'}]
        test_case = app.extract_comment_from_line_list(line_list, app.python_comment)
        self.assertEqual(test_case[0]['line'], '"""line1line2')

    # def test_test_extract_comment_from_multi_line(self):
    #     line_list = [{'line: ''}]

    def test_extract_comment_from_c_comment(self):
        line_list= [{"line":"/*** Main encode function ***/", "location": "random"},
                    {"line":"enum punycode_status punycode_encode(punycode_uint input_length", "location": "random"},
                    {"line": "const punycode_uint input[]", "location": "random"},
                    {"line": "const unsigned char case_flags[]", "location": "random"},
                    {"line": "punycode_uint* output_length", "location": "random"},
                    {"line": "char output[]) {", "location": "random"},
                    {"line": "punycode_uint n, delta, h, b, out, max_out, bias, j, m, q, k, t;", "location": "random"},
                    {"line": "/* Initialize the state: */", "location": "random"}]

        test_case = app.extract_comment_from_line_list(line_list, app.c_comment)
        # TODO strip of symbols and whitespace for test1
        self.assertEqual(test_case[-1]['line'], '* Initialize the state: *')
        test2 = app.strip_comment_of_symbols(test_case[0]['line'], app.c_comment)
        test2 = app.remove_starting_whitespace(test2)
        self.assertEqual(test2, 'Main encode function ')

def main():
    # Create a test suit
    suit = unittest.TestLoader().loadTestsFromTestCase(test_app)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
