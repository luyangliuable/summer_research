import os
from comment_parser import comment_parser
from typing import List, TypeVar

T = TypeVar("T")

wildcard_identifier = '*'

def extract_comment_from_line(files: List[T], language: str) -> List[T]:
    res = []
    for file in files:
        print(comment_parser.extract_comments(file, mime='text/x-python'))
        res.append(comment_parser.extract_comments(file, mime='text/x-python'))
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



f = open("script.py", "r")
print(checkFileSameFormat("a.py", "b.py"))
found_files = searchFile('*.py', '.')
print(found_files)
found_comments = extract_comment_from_line(found_files, 'python')
print(found_comments)
