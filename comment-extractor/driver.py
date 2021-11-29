import app

###############################################################################
#               The driver for the comment-extractor application              #
###############################################################################

# extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.shell_comment, "./artefacts/firefox_makefile")
# extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.python_comment, "./artefacts/firefox_python")
# extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.makefile_comment, "./artefacts/firefox_shell")
# extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.shell_comment, "./artefacts/firefox_shell")
# extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.cpp_comment, "./artefacts/firefox_cpp")
# extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.javascript_comment, "./artefacts/firefox_javascript")
extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/firefox-source/', app.gradle_comment, "./test")
