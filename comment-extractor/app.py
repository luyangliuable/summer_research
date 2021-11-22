import os
from comment_parser import comment_parser
from typing import List, TypeVar

T = TypeVar("T")

def extract_comment_from_line(file: str) -> str:
    return comment_parser.extract_comments(file, mime='text/x-python')



def searchFile(fileName: str, path: str):
    print(path)
    for root, dirs, files in os.walk(path):
        print(files)
        print(root)
        print('Looking in:',root)
        for Files in files:
            try:
                found = Files.find(fileName)
                # print(found)
                if found != -1:
                    print()
                    print(fileName, 'Found\n')
                    break
            except:
                exit()

f = open("script.py", "r")
searchFile('script.py', './test_folder')
# print(f.read())
# print(extract_comment_from_line('./test-folder/script.py'))
