import app

###############################################################################
#               The driver for the comment-extractor application              #
###############################################################################

extracted_comments = app.extract_comment_from_path('/home/luyang/Documents/linux/', app.makefile_comment, "./comment_csv_files/linux_kernal_makefile")
extracted_comments2 = app.extract_comment_from_path('/home/luyang/Documents/linux/', app.perl_comment, "./comment_csv_files/linux_kernal_perl")
extracted_comments3 = app.extract_comment_from_path('/home/luyang/Documents/linux/', app.shell_comment, "./comment_csv_files/linux_kernal_shell")
