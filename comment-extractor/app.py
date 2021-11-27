import os
from comment_parser import comment_parser
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

wildcard_identifier = '*'

c_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": ['//', '/*'],
    "format": 'c'
}

python_comment = {
    "multiline_start": '"""',
    "multiline_end": '"""',
    "single_line": ['#', '"""'],
    "format": 'py'
}

asm_comment = {
    "multiline_start": '/*',
    "multiline_end": '*/',
    "single_line": [';', '/*'],
    "format": 'asm'
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
    "format": 'makefile'
}

shell_comment = makefile_comment

perl_comment = {
    "multiline_start": '=',
    "multiline_end": '=',
    "single_line": ['#', '='],
    "format": 'pl'
}

def get_every_line_from_file(file: str) -> List[T]:
    thefile = open(file, 'r')
    lines = thefile.readlines()
    for line_number in range(len(lines)):
        lines[line_number] = {
            'line': lines[line_number],
            'location': file + ": " + str(line_number+1)
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
    dir = "./comment_csv_files/linux_kernal_makefile"
    comment_dir = create_comment_file(output_dir)

    files = files + searchFile('*' + language["format"], directory)

    # if language is python_comment:
    #     files = files + searchFile('*.py', directory)
    # elif language is c_comment:
    #     files = files + searchFile('*.c', directory)
    # elif language is asm_comment:
    #     files = files + searchFile('*.asm', directory)
    # elif language is makefile_comment:
    #     files = files + searchFile('*.makefile', directory)

    line_counter = 0;
    max_line_per_file = 50000
    for file in files:
        if line_counter > max_line_per_file:
            comment_dir = create_comment_file(output_dir)
            line_counter = 0
        # print("extracting comment from: " + file)
        lines_in_file = get_every_line_from_file(file)
        comments_in_file = extract_comment_from_line_list(lines_in_file, language)
        comments = [{'line': strip_comment_of_symbols(comment['line'], language), 'location': comment['location']} for comment in comments_in_file]
        print(comments)
        write_comment_file(comments_in_file, comment_dir)
        line_counter += len(comments_in_file)


def extract_comment_from_line_list(lines: List[T], language: dict) -> List[T]:
    """extracts the comment from a list of lines

    Keyword Arguments:

    lines -- list of lines to extract the comment from. It contains the line as well as the file location
    languages -- the language the lines are written in
    """

    multiline_comment = False
    res = []

    for line in lines:
        if check_triggers_multiline_comment(line['line'], language["multiline_start"], language["multiline_end"]):
            multiline_comment = not multiline_comment

        if multiline_comment and not check_if_comment_is_empty(line['line'], language):
            comment = line
        else:
            comment = {
                'line': find_text_enclosed_inside(line['line'], language["single_line"]),
                'location': line['location']
            }

        if comment and not check_if_comment_is_empty(comment, language):
            res.append(comment)
            # res.append(comment_parser.extract_comments(file, mime='text/x-python'))
    return res;

def searchFile(fileName: str, path: str) -> List[T]:
    """Search a root directory for a particular file

    Keyboard Arguments:
    fileName -- name of the file to search for
    path -- path from which to search the file
    """
    # print("Searching in path: " + path + " for " + fileName)
    res = []
    for root, dirs, files in os.walk(path):
        if fileName[0] == wildcard_identifier:
            for file in files:
                sameFormat = checkFileSameFormat(fileName, file)
                if sameFormat:
                    res.append(root + "/" + file)
        else:
            for file in files:
                if file == fileName:
                    res.append(root + "/" + file)

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
    while fileOne[-counter] != "." and fileTwo[-counter] != "." and counter < min(len(fileOne), len(fileTwo)):
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
    triggers_closing_multiline = False
    multiline_sexp_length = len(multiline_sexp)
    res = ""
    start_of_comment = None
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

def find_text_enclosed_inside(line: str, sexp: List[str]) -> str:
    """Find a text contained inside a sexp (s-expression)

    Keyword Arguments:
    line: the line from which to find string enclosed inside the s-expression
    sexp: s-expression that opens a multi-line comment incl. for example ({})[]
    """
    line_comment_active = False
    res = ""

    for sexp in sexp:
        sexp_length = len(sexp)
        start_of_comment = None
        for which_line_column in range(len(line)):
            sliding_window = ""
            for which_sexp_column in range(sexp_length):
                if which_sexp_column + which_line_column < len(line):
                    assert which_line_column + which_sexp_column >=0
                    assert which_line_column + which_sexp_column < len(line)
                    sliding_window += line[which_line_column + which_sexp_column]

            if sliding_window in sexp:
                line_comment_active = not line_comment_active
                start_of_comment = which_line_column + sexp_length

            not_over_end_of_line = False
            if start_of_comment is not None:
                current_line_in_word = which_line_column - start_of_comment + sexp_length
                not_over_end_of_line = current_line_in_word <= len(line)

            if line_comment_active and sliding_window not in sexp and not_over_end_of_line:
                if which_line_column >= start_of_comment:
                    res += line[which_line_column]

    return res

def create_comment_file(target: str) -> str:
    counter = 0
    res = ""
    while True:
        filename = "commentfile" + str(counter) + ".csv"
        if len(searchFile(filename, ".")) == 0:
            print("creating new comment file " + filename)
            res = target + "/" + filename
            f = open(res, "a")
            f.write("")
            f.close()
            break
        counter += 1

    return res

def strip_comment_of_symbols(comment: str, language: dict) -> str:
    res = ""
    print(comment)
    comment = comment.strip("\n")
    for char in comment:
        if not char in language["multiline_start"] or not char in language["multiline_end"]:
            res = res + char;

    # comment = comment.lstrip(" ")

    return res

def check_if_comment_is_empty(comment: str, language: dict) -> bool:
    comment = comment['line']
    comment = strip_comment_of_symbols(comment, language)
    comment = comment.strip(" ")
    if comment == "":
        return True
    return False

def write_comment_file(lines_of_comment: List[T], target: str):
        f = open(target, "a")
        for comment in lines_of_comment:
            comment_text = comment['line']
            filepath = comment['location']
            f.write(comment_text + " " + filepath + '\n')
        f.close()


# file = create_comment_file("./comment_csv_files")
# write_comment_file(["a", "basdads"], file)

# write_comment_file(['a', 'b'], "./comment_csv_files")

# extracted_comments = extract_comment_from_path('/home/luyang/Documents/linux', c_comment, "./comment_csv_files/linux_kernal_c2")

# a = extract_comment_from_line_list(['asdasd', '/* asdasd', "/* ", "*"], c_comment)
# extracted_comments = extract_comment_from_path('./test-folder', c_comment, "./")

# extracted_comments = extract_comment_from_path('./test-folder', c_comment, "./")
# print(extracted_comments)

extracted_comments = extract_comment_from_path('./test-folder', python_comment, './')

# comments = extract_comment_from_line([ './test-folder' ], 'python')
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
