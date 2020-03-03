import configparser

from .log_n_save2file import log_file


def config_file(file_path, request_attribute):
    config = configparser.ConfigParser()
    config.read(file_path)
    if request_attribute == 'db_name':
        try:
            return config['DB']['name']
        except KeyError:
            event = "ошибка в чтении конфиг файла при обращении DB_files_old -> Name"
            print(event)
            log_file(event)
    if request_attribute == 'xml_file':
        try:
            return config['XML']['name']
        except KeyError:
            event = "ошибка в чтении конфиг файла при обращении XML -> Name"
            print(event)
            log_file(event)
    elif request_attribute == 'ip':
        try:
            return config['TCP']['ip']
        except KeyError as e:
            print(e.args[0])
            event = "ошибка в чтении конфиг файла при обращении TCP -> ip"
            print(event)
            log_file(event)
    elif request_attribute == 'port':
        try:
            return config['TCP']['port']
        except KeyError:
            event = "ошибка в чтении конфиг файла при обращении TCP -> port"
            print(event)
            log_file(event)
    elif request_attribute == 'timeout':
        try:
            return config['TIME']['timeout']
        except KeyError:
            event = "ошибка в чтении конфиг файла при обращении TIME -> timeout"
            print(event)
            log_file(event)
    elif request_attribute == 'fsrar_id':
        try:
            return config['UTM']['fsrar_id']
        except KeyError:
            event = "ошибка в чтении конфиг файла при обращении UTM -> fsrar_id"
            print(event)
            log_file(event)
    else:
        print('неправильно указан запрос к .ini файлу!')


class Config:
    def __init__(self, file_path):
        self.ip = config_file(file_path, 'ip')
        self.port = config_file(file_path, 'port')
        self.DB_name = f"{config_file(file_path, 'db_name')}"
        self.timeout = config_file(file_path, 'timeout')
        self.xml_name = config_file(file_path, 'xml_file')
        self.fsrar_id = config_file(file_path, 'fsrar_id')
        self.name = file_path

    def __str__(self):
        return f"{self.name}"
