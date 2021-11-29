import os
import csv
import chardet
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

###############################################################################
#                    Dictionaries for programming languages                   #
###############################################################################

WILDCARD_IDENTIFIER = '*'

c_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": ['//', '/*'],
    "format": 'c',
    "language": "c"
}

kotlin_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": ['//', '/*'],
    "format": 'kt',
    "language": "kotlin"
}

cpp_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": ['//', '/*'],
    "format": 'cpp',
    "language": "c++"
}


javascript_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": ['//', '/*'],
    "format": 'js',
    "language": "javascript"
}


gradle_comment = {
    "multiline_start": '',
    "multiline_end": '',
    "single_line": ['//'],
    "format": 'gradle',
    "language": "gradle"
}


java_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": ['//', '/*'],
    "format": 'java',
    "language": "java"
}

build_comment = {
    "multiline_start": '',
    "multiline_end": '',
    "single_line": ['#'],
    "format": 'build',
    "language": "build"
}

python_comment = {
    "multiline_start": '"""',
    "multiline_end": '"""',
    "single_line": ['#', '"""'],
    "format": 'py',
    "language": "python"
}

asm_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": [';', '/*'],
    "format": 'asm',
    "language": "assembly"

}


""" assume (no comment like this for makefile and shell):
# This is the first line of a comment \
and this is still part of the comment \
as is this, since I keep ending each line \
with a backslash character
"""
makefile_comment = {
    "multiline_start": '',
    "multiline_end": '',
    "single_line": ['#'],
    "format": 'makefile',
    "language": "makefile"
}

shell_comment = {
    "multiline_start": '',
    "multiline_end": '',
    "single_line": ['#'],
    "format": 'sh',
    "language": "shell"
}

perl_comment = {
    "multiline_start": '=',
    "multiline_end": '=',
    "single_line": ['#', '='],
    "format": 'pl',
    "language": "perl"
}


def get_every_line_from_file(filename: str) -> List[T]:

    ###############################################################################
    #                         getting encoding of the file                        #
    ###############################################################################

    lines = []
    with open(filename, 'rb') as thefile:
        encoding = chardet.detect(bytes(thefile.read()))['encoding']

    try:
        thefile = open(filename, 'r', encoding=encoding)
        lines = thefile.readlines()
    except:
        try:
            print("Trouble decoding file " + filename + " now attempting to use utf-8")
            with open(filename, 'r', encoding="utf-8" ) as thefile:
                lines = thefile.readlines()
        except:  # UnsupportEncodingException:
            print("failed to decode file" + filename)

    if len(lines) != 0:
        for line_number in range(len(lines)):  # enumerate(line)
            lines[line_number] = {
                'line': lines[line_number].strip('\n'),
                'location': filename + ": " + str(line_number+1)
            }
    return lines


def extract_comment_from_path(directory: str, language: dict, output_dir: str):
    """Extracts all comments from file contained inside a path

    Keyword Arguments:

    directory -- the root directory to search from
    language

    language -- the programming language to search in
    """
    files = []
    comment_dir = create_comment_file(output_dir, language)

    files = files + search_file('*' + language["format"], directory)

    # if language is python_comment:
    #     files = files + search_file('*.py', directory)
    # elif language is c_comment:
    #     files = files + search_file('*.c', directory)
    # elif language is asm_comment:
    #     files = files + search_file('*.asm', directory)
    # elif language is makefile_comment:
    #     files = files + search_file('*.makefile', directory)

    line_counter = 0

    # The maximum line of code for each csv file ###############################
    max_line_per_file = 50000
    for file in files:
        if line_counter > max_line_per_file:
            comment_dir = create_comment_file(output_dir, language)
            line_counter = 0

        lines_in_file = get_every_line_from_file(file)
        comments_in_file = extract_comment_from_line_list(lines_in_file, language)

        # Strip comment of symbols ####################################################
        comments = [{'line': strip_comment_of_symbols(comment['line'], language), 'location': comment['location']} for comment in comments_in_file]

        # Strip comment of starting whitespace ########################################
        comments = [{'line': remove_starting_whitespace(comment['line']), 'location': comment['location']} for comment in comments]
        # comments = [{'line': remove_starting_whitespace(comment['line']), 'location': comment['location']} for comment in comments]
        write_comment_file(comments, comment_dir)
        line_counter += len(comments)


def extract_comment_from_line_list(lines: List[T], language: dict) -> List[T]:
    """extracts the comment from a list of lines

    if is a multiline comment, accumulate the multiline comment and return as a single line
    if is a single line comment, return as a single line

    Keyword Arguments:

    lines -- list of lines to extract the comment from. It contains the line as well as the file location
    languages -- the language the lines are written in
    """

    res = []
    multiline_comment = False

    # for line in lines:
    #     comment = ""
    #     if check_triggers_multiline_comment(line['line'], language["multiline_start"], language["multiline_end"]):
    #         multiline_comment = not multiline_comment

    #     if multiline_comment:
    #         comment = {
    #             'line': line['line'],
    #             'location': line['location']
    #         }
    #     elif comment == "":
    #         comment = {
    #             'line': find_text_enclosed_inside(line['line'], language["single_line"]),
    #             'location': line['location']
    #         }


    #     if comment != "" and not check_if_comment_is_empty(comment, language):
    #         assert comment.__class__ is dict, "class of comment must be stored in dictionary"
    #         res.append(comment)
    # return res;

    single_multiline_comment = ""
    for line in lines:
        comment = ""
        if check_triggers_multiline_comment(line['line'], language["multiline_start"], language["multiline_end"]):
            if not multiline_comment:
                multiline_comment = True
            else:
                comment = {
                    'line': single_multiline_comment,
                    'location': line['location']
                }
                multiline_comment = False

        if multiline_comment:
            single_multiline_comment += line['line'].strip("\n")
        elif comment == "":
            comment = {
                'line': find_text_enclosed_inside(line['line'], language["single_line"]),
                'location': line['location']
            }

        if comment and not check_if_comment_is_empty(comment, language):
            assert comment.__class__ is dict, "class of comment must be stored in dictionary"
            res.append(comment)
            # res.append(comment_parser.extract_comments(file, mime='text/x-python'))
    return res


def search_file(file_name: str, path: str) -> List[T]:
    """Search a root directory for a particular file

    Keyboard Arguments:
    file_name -- name of the file to search for
    path -- path from which to search the file
    """
    # print("Searching in path: " + path + " for " + file_name)
    res = []
    for root, dirs, files in os.walk(path):
        if file_name[0] == WILDCARD_IDENTIFIER:
            for file in files:
                same_format = check_file_is_same_format(file_name, file)
                if same_format:
                    if root[-1] != "/" and file[0] != "/":
                        res.append(root + "/" + file)
                    else:
                        res.append(root + file)
        else:
            for file in files:
                if file == file_name:
                    if root[-1] != "/" and file[0] != "/":
                        res.append(root + "/" + file)
                    else:
                        res.append(root + file)

            found = file.find(file_name)

            if found != -1:
                break
    return res


def check_file_is_same_format(fileOne: str, fileTwo:str) -> bool:
    """Checks if file1 and file2 are of the same format

    Keyword Arguments:
    fileOne -- the first file in the comparison
    fileTwo -- the second file in the comparison
    """
    counter = 1
    while fileOne[-counter] != "." and counter < min(len(fileOne), len(fileTwo)):
        if fileOne[-counter] != fileTwo[-counter]:
            return False
        counter += 1

    return True


def check_triggers_multiline_comment(line: str, multiline_sexp: str, multiline_closing_sexp: str) -> bool:
    """checks if a particular line triggers the start of a multi-line comment

    Keyword Arguments:
    line -- the line to examine
    multiline_sexp -- the sexp that dictates the start of multi-line comment
    """

    triggers_multiline = False
    # triggers_closing_multiline = False
    multiline_sexp_length = len(multiline_sexp)
    # res = ""
    # start_of_comment = None
    for which_line_column in range(len(line)):
        sliding_window = ""
        for which_sexp_column in range(multiline_sexp_length):
            if which_sexp_column + which_line_column < len(line):
                sliding_window += line[which_line_column + which_sexp_column]

        if multiline_sexp is not multiline_closing_sexp:
            if sliding_window in multiline_sexp:
                triggers_multiline = not triggers_multiline

            if sliding_window in multiline_closing_sexp:
                triggers_multiline = not triggers_multiline

        elif multiline_sexp is multiline_closing_sexp:
            if sliding_window in multiline_sexp:
                triggers_multiline = not triggers_multiline

    return triggers_multiline


def find_text_enclosed_inside(line: str, sexpressions: List[str]) -> str:
    """Find a text contained inside a sexp (s-expression)

    Keyword Arguments:
    line: the line from which to find string enclosed inside the s-expression
    sexp: s-expression that opens a multi-line comment incl. for example ({})[]
    """
    line_comment_active = False
    res = ""

    for sexp in sexpressions:
        sexp_length = len(sexp)
        start_of_comment = None
        for which_line_column in range(len(line)):
            sliding_window = ""
            for which_sexp_column in range(sexp_length):
                if which_sexp_column + which_line_column < len(line):
                    assert which_line_column + which_sexp_column >= 0
                    assert which_line_column + which_sexp_column < len(line)
                    sliding_window += line[which_line_column + which_sexp_column]

            if sliding_window == sexp:
                print(sliding_window + " compare " + sexp)
                print(sliding_window == sexp)
                print(sliding_window is sexp)
                line_comment_active = not line_comment_active
                start_of_comment = which_line_column + sexp_length

            not_over_end_of_line = False
            if start_of_comment is not None:
                current_line_in_word = which_line_column - start_of_comment + sexp_length
                not_over_end_of_line = current_line_in_word <= len(line)

            if line_comment_active and not_over_end_of_line:
                if sliding_window not in sexp:
                    res += line[which_line_column]

    return res


def create_comment_file(target: str, language) -> str:
    """Create a comment file in the target directory

    Keyword Arguments:

    target -- the target directory
    """
    counter = 0
    res = ""

    fieldnames = ['line', 'location']
    while True:
        filename = "commentfile" + str(counter) + ".csv"
        if len(search_file(filename, ".")) == 0:
            print("creating new comment file " + filename)
            res = target + "/" + filename
            f = open(res, "a")
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            f.write(language['language'] + '\n')
            writer.writeheader()
            f.close()
            break
        counter += 1

    return res


def strip_comment_of_symbols(comment: str, language: dict) -> str:
    """Strip the comment of all programming language symbols

    Keyword Arguments:

    comment -- A string of comment

    language -- the programming language to search in
    """
    res = ""
    comment = comment.strip("\n")
    for char in comment:
        if char not in language["multiline_start"] or char not in language["multiline_end"]:
            res = res + char

    return res


def remove_starting_whitespace(comment: str) -> str:
    """Remove all the whitespace before the actual comment

    Keyword Arguments:

    comment -- A string of comment
    """
    trailing_whitespace = True
    res = ""

    for char in comment:
        if char != " ":
            trailing_whitespace = False

        if not trailing_whitespace:
            res += char

    return res


def check_if_comment_is_empty(comment: dict, language: dict) -> bool:
    """Check if the comment inside the comment is empty

    Keyword Arguments:

    comment -- A dictionary containing the comment as well as the location the comment is from
    language -- The language the comment is written in
    """
    if comment.__class__ is dict:
        Exception("class of comment must be stored in dictionary")
    comment = comment['line']
    assert comment.__class__ is str, "comment must be in string form to be processed: " + str(comment)
    comment = strip_comment_of_symbols(comment, language)
    for symbol in language["single_line"]:
        comment = comment.strip(symbol)
        comment = comment.strip(" ")
    if comment in ('', '\n'):

        return True
    return False


def write_comment_file(lines_of_comment: List[T], target: str):
    """Append a list comments to a file
    Keyword Arguments:

    lines_of_comment -- A list containing comment dictionaries
    target -- the target directory
    """

    fieldnames = ['line', 'location']

    with open(target, "a", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerows(lines_of_comment)
    file.close()
