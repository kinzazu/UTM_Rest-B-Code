

def log_file(file_path): # file path or just name if it's in folder.
    try:
        file = open(file_path, 'x')
    except FileExistsError:
        print('file already exist')
        file = open(file_path, 'a')
    else:
        print('OK')
    file.write("\n some_function ")
    file.close()

# log_file('log_files/1223.txt')
