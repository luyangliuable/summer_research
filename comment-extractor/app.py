import os
from comment_parser import comment_parser
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

wildcard_identifier = '*'

def get_every_line_from_file(file: str) -> List[T]:
    file = open(file, 'r')
    lines = file.readlines()
    return lines

def extract_comment_from_path(directory: str, language: str) -> List[T]:
    """Extracts all comments from file contained inside a path

    Keyword Arguments:

    directory -- the root directory to search from
    language

    language -- the programming language to search in
    """
    files = []

    if language == 'python':
        files = files + searchFile('*.py', directory)
    elif language == 'c':
        files = files + searchFile('*.c', directory)

    lines = []
    for file in files:
        lines = lines + get_every_line_from_file(file)

    comments = extract_comment_from_line_list(lines, language)

    return comments


def extract_comment_from_line_list(lines: List[T], language: str) -> List[T]:
    """extracts the comment from a list of lines

    Keyword Arguments:

    lines -- list of lines to extract the comment from
    languages -- the language the lines are written in
    """

    multiline_comment = False

    res = []

    for line in lines:
        if language == 'python':
            if check_triggers_multiline_comment(line, '"""'):
                multiline_comment = not multiline_comment

            if multiline_comment:
                comment = line
            else:
                comment = find_text_enclosed_inside(line, "#")

        elif language == 'c':
            if check_triggers_multiline_comment(line, "/*"):
                multiline_comment = not multiline_comment

            if multiline_comment:
                comment = line
            else:
                comment = find_text_enclosed_inside(line, '//')

        if comment:
            res.append(comment)
            # res.append(comment_parser.extract_comments(file, mime='text/x-python'))
    return res;

def searchFile(fileName: str, path: str) -> List[T]:
    """Search a root directory for a particular file

    Keyboard Arguments:
    fileName -- name of the file to search for
    path -- path from which to search the file
    """
    print("Searching in path: " + path + " for " + fileName)
    res = []
    for root, dirs, files in os.walk(path):
        if fileName[0] == wildcard_identifier:
            for file in files:
                sameFormat = checkFileSameFormat(fileName, file)
                if sameFormat:
                    res.append(root + "/" + file)
        else:
            found = file.find(fileName)
            if found != -1:
                break
    return res

def checkFileSameFormat(fileOne: str, fileTwo:str) -> bool:
    """Checks if file1 and file2 are of the same format

    Keyword Arguments:
    fileOne -- the first file in the comparison
    fileTwo -- the second file in the comparison
    """
    counter = 1
    while fileOne[-counter] != "." and fileTwo[-counter] != "." and counter <= min(len(fileOne), len(fileTwo)):
        if fileOne[-counter] != fileTwo[-counter]:
            return False
        counter += 1

    return True

def check_triggers_multiline_comment(line:str, multiline_sexp: str) -> bool:
    """checks if a particular line triggers the start of a multi-line comment

    Keyword Arguments:
    line -- the line to examine
    multiline_sexp -- the sexp that dictates the start of multi-line comment
    """

    triggers_multiline = False
    multiline_sexp_length = len(multiline_sexp)
    res = ""
    start_of_comment = None
    for which_line_column in range(len(line)):
        comment_specifier = ""
        for which_sexp_column in range(multiline_sexp_length):
            if which_sexp_column + which_line_column < len(line):
                comment_specifier += line[which_line_column + which_sexp_column]

        if comment_specifier in multiline_sexp:
            triggers_multiline = not triggers_multiline

    return triggers_multiline

def find_text_enclosed_inside(line: str, sexp: str) -> str:
    """Find a text contained inside a sexp (s-expression)

    Keyword Arguments:
    line: the line from which to find string enclosed inside the s-expression
    sexp: s-expression incl. for example ({})[]
    """
    line_comment_active = False

    sexp_length = len(sexp)
    res = ""
    start_of_comment = None
    for which_line_column in range(len(line)):
        comment_specifier = ""
        for which_sexp_column in range(sexp_length):
            if which_sexp_column + which_line_column < len(line):
                assert which_line_column + which_sexp_column >=0
                assert which_line_column + which_sexp_column < len(line)
                comment_specifier += line[which_line_column + which_sexp_column]

        # comment_specifier = [str(line[w+which_column]) + str(line[which_column+w+1]) if w+which_column+1 < len(line) else "" for w in range(sexp_length)][0]

        if line_comment_active and comment_specifier not in sexp and which_line_column - start_of_comment + sexp_length <= len(line):
            if which_line_column >= start_of_comment:
                res += line[which_line_column]

        if comment_specifier in sexp:
            line_comment_active = not line_comment_active
            start_of_comment = which_line_column + sexp_length
        else:
            pass
    return res


extracted_comments = extract_comment_from_path('./test-folder', 'c')
print(check_triggers_multiline_comment('"""ssdsad', '"""'))
print(extracted_comments)

# comments = extract_comment_from_line([ './test-folder/a.py' ], 'python')
# print(comments)

# loc = get_every_line_from_file('app.py')[

# comment = find_text_enclosed_inside("asd sad ///*assad", "///*")
# print("comment is: " + comment)


# comment = find_text_enclosed_inside("asd sad ///*assad", "///*")
# print("comment is: " + comment)

# f = open("script.py", "r")
# print(checkFileSameFormat("a.py", "b.py"))
# found_files = searchFile('*.py', '.')
# print(found_files)

# found_comments = extract_comment_from_line_list([ "#sdsada", "#asdasd"], 'python')
# print(found_comments)
