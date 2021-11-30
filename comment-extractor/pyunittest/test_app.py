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
        test_case = app.strip_comment_of_symbols(test_case[0]['line'], app.python_comment)
        test_case = app.remove_starting_whitespace(test_case)
        self.assertEqual(test_case, 'line1 line2  ')

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


    def test_extract_multiline_comment_from_c(self):
        line_list= [
            {"line":"/* Main encode function", "location": "random"},
            {"line": "beep boop", "location": "random"},
            {"line": "Initialize the state: */", "location": "random"},
        ]

        test_case = app.extract_comment_from_line_list(line_list, app.c_comment)
        test2 = app.strip_comment_of_symbols(test_case[0]['line'], app.c_comment)
        test2 = app.remove_starting_whitespace(test2)
        self.assertEqual(test2, 'Main encode function beep boop Initialize the state:  ')


    def test_check_trigger_multiline_comment_c(self):
        test_case = app.check_triggers_multiline_comment('/*', app.c_comment['multiline_start'], app.c_comment['multiline_end'])
        test_case2 = app.check_triggers_multiline_comment('*/', app.c_comment['multiline_start'], app.c_comment['multiline_end'])
        test_case3 = app.check_triggers_multiline_comment('/* no */', app.c_comment['multiline_start'], app.c_comment['multiline_end'])
        self.assertTrue(test_case)
        self.assertTrue(test_case2)
        self.assertFalse(test_case3)


    def test_iterate_dictionary_for_header(self):
        test_case = app.iterate_dictionary_for_header(app.languages)
        self.assertEqual(['c', 'kotlin', 'c++', 'javascript', 'gradle', 'build', 'python', 'assembly', 'makefile', 'shell', 'perl', 'java'], test_case)

    def test_save_to_dictionary(self):
        test_case = app.save_in_dict('line', 'location', 'language')
        self.assertTrue(test_case, {"line": 'line', "location": 'location', 'language': 'language'})

    # def test_wrong_files_c(self):
    #     location = "./test-folder/test.c"
    #     test_case = app.get_every_line_from_file(location)
    #     self.assertEqual(test_case[-1], {'line': "#include <linux/parman.h>", 'location': './test-folder/test.c', 'language': 'c'})

    def test_extract_wrong_comments_c(self):
        location = "./test-folder/test.c"
        test_case = app.get_every_line_from_file(location)
        test_case = app.extract_comment_from_line_list(test_case, app.c_comment)
        self.assertNotEqual(test_case[-1]['line'], "wrong comment")

    def test_write_wrong_comments_c(self):
        comment = [{"line": "/* * lib/parman.c - Manager for linear priority array areas */", "location": "random", "language": 'c'}, {"line": "/* test 1 */", "location": "random", "language": 'c'}]

        location = app.create_comment_file('./', app.c_comment)
        app.write_comment_file(comment, location)

    def test_full_write_file(self):
        file = "./test-folder/parman.c"
        comment_dir = './dump.csv'
        lines_in_file = app.get_every_line_from_file(file)
        comments_in_file = app.extract_comment_from_line_list(lines_in_file, app.c_comment)

        # Strip comment of symbols ####################################################
        comments = [app.save_in_dict(app.strip_comment_of_symbols(comment['line'], app.c_comment), comment['location'], app.c_comment) for comment in comments_in_file]
        # comments = [{'line': strip_comment_of_symbols(comment['line'], language), 'location': comment['location']} for comment in comments_in_file]

        # Strip comment of starting whitespace ########################################
        # comments = [remove_starting_whitespace(comments[i]['line']) for i in range(len( comments ))]
        comments = [app.save_in_dict(app.remove_starting_whitespace(comment['line']), comment['location'], app.c_comment['language']) for comment in comments]

        app.write_comment_file(comments, comment_dir)

def main():
    # Create a test suit
    suit = unittest.TestLoader().loadTestsFromTestCase(test_app)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
