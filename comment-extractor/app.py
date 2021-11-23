import os
from comment_parser import comment_parser
from typing import List, TypeVar

T = TypeVar("T")

def extract_comment_from_line(file: str) -> str:
    return comment_parser.extract_comments(file, mime='text/x-python')

def searchFile(fileName: str, path: str) -> List[T]:
    print("Searching in path: " + path + " for " + fileName)
    res = []
    for root, dirs, files in os.walk(path):
        if fileName[0] == '*':
            for Files in files:
                sameFormat = checkFileSameFormat(fileName, Files)
                if sameFormat:
                    # res.append(Files)
                    res.append("./" + (dirs[0] + "/" if len(dirs) > 0 else "") + Files)
        else:
            found = Files.find(fileName)
            if found != -1:
                # res.append(fileName)
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
print(searchFile('*.py', './'))
# print(f.read())
# print(extract_comment_from_line('./test-folder/script.py'))
