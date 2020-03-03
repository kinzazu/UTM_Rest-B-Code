import os


class Path2File:
    def __init__(self):
        self.path = os.getcwd()
        self.main_folder = self.get_main_folder()

    def get_main_folder(self):
        main_folder = os.path.split(self.path)[0]
        main_folder = os.path.normpath(main_folder)
        return main_folder

    def set_path_file(self, folder='my_files', file='', subfolder=None):
        if subfolder is None:
            path_file = os.path.join(self.main_folder, folder, file)
        else:
            path_file = os.path.join(self.main_folder, folder, subfolder, file)
        path_file = os.path.normpath(path_file)
        return path_file
'C:\\Users\\nikol\\Documents\\GitHub\\UTM_Rest-B-Code\\my_files\\ini\\conf.ini'
'C:\\Users\\nikol\\Documents\\GitHub\\UTM_Rest-B-Code\\my_files\\ini\\conf.ini'
