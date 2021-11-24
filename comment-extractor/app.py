import os
from comment_parser import comment_parser
from typing import List, TypeVar

T = TypeVar("T")

wildcard_identifier = '*'

def extract_comment_from_line(files: List[T], language: str) -> List[T]:
    res = []
    for file in files:
        lines = get_every_line_from_file(file)
        for line in lines:
            comment = find_text_enclosed_inside(line, "#")
            print(comment)
            # print(comment_parser.extract_comments(file, mime='text/x-python'))
            # res.append(comment_parser.extract_comments(file, mime='text/x-python'))
    return res;

def searchFile(fileName: str, path: str) -> List[T]:
    print("Searching in path: " + path + " for " + fileName)
    res = []
    for root, dirs, files in os.walk(path):
        if fileName[0] == wildcard_identifier:
            for file in files:
                sameFormat = checkFileSameFormat(fileName, file)
                if sameFormat:
                    print(root)
                    res.append(root + "/" + file)
        else:
            found = file.find(fileName)
            if found != -1:
                break
    return res

def checkFileSameFormat(fileOne: str, fileTwo:str) -> bool:
    counter = 1
    while fileOne[-counter] != "." and fileTwo[-counter] != "." and counter <= min(len(fileOne), len(fileTwo)):
        if fileOne[-counter] != fileTwo[-counter]:
            return False
        counter += 1

    return True


def find_text_enclosed_inside(line_of_code: str, sexp: str) -> str:
    active = False
    literal_specifiers = "\""
    res = ""
    for i in line_of_code:

        if active and i not in sexp:
            res += i
        if i in sexp:
            active = not active
        else:
            pass
    return res

def get_every_line_from_file(file: str) -> List[T]:
    file = open(file, 'r')

    lines = file.readlines()
    return lines

extract_comment_from_line([ 'app.py' ], 'python')

# loc = get_every_line_from_file('app.py')

# for line in loc:
#     comment = find_text_enclosed_inside(line, "#")
#     print("comment is: " + comment)

# f = open("script.py", "r")
# print(checkFileSameFormat("a.py", "b.py"))
# found_files = searchFile('*.py', '.')
# print(found_files)

# found_comments = extract_comment_from_line(found_files, 'python')
# print(found_comments)
