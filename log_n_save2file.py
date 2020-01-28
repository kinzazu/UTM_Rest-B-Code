import configparser
import datetime
import os


class Config:
    def __init__(self,file_path):
        self.ip = self.config_file(file_path, 'ip')
        self.port = self.config_file(file_path, 'port')
        self.DB_name = self.config_file(file_path, 'db_name')
        self.timeout = self.config_file(file_path, 'timeout')
        self.xml_name = self.config_file(file_path, 'xml_file')
        self.fsrar_id = self.config_file(file_path, 'fsrar_id')
        self.name = file_path

    def __str__(self):
        return f"{self.name}"

    def config_file(self, file_path, request_attribute):
        config = configparser.ConfigParser()
        config.read(file_path)
        if request_attribute == 'db_name':
            try:
                return config['DB']['name']
            except KeyError:
                event = "ошибка в чтении конфиг файла при обращении DB -> Name"
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
            except KeyError:
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


def create_log_file():
    txt_file_path = 'Logs/{}.txt'.format(str(datetime.date.today()))
    while True:
        try:
            file = open(txt_file_path, 'x')

        except FileExistsError:
            file = open(txt_file_path, 'a')
            break
        except FileNotFoundError:
            path = os.getcwd()
            os.mkdir('{}\\Logs'.format(path))
            print('created directory')
            continue
        else:
            break
    return file


def log_file(event):  # file path or just name if it's in folder.
    file = create_log_file()
    file.write(f"\n {datetime.datetime.now().isoformat(timespec= 'seconds')} {event}")
    file.close()


def save_xml(xml_text, type_file: int):
    time = datetime.datetime.now()
    # print(time)
    if type_file == 1:
        xml_file_path = 'xml/{}-{}-{} T{}-{}-{}-list.xml'.format(time.year, time.month, time.day,
                                                                 time.hour, time.day, time.second)
    elif type_file == 2:
        xml_file_path = 'xml/{}-{}-{} T{}-{}-{}-element.xml'.format(time.year, time.month, time.day,
                                                                    time.hour, time.day, time.second)
    elif type_file == 3:
        xml_file_path = 'xml/QueryFormBHistory.xml'
    else:
        print("ошибка в типе файла для сохранения xml")
    while True:
        try:
            file = open(xml_file_path, 'w')
        except FileNotFoundError:
            path = os.getcwd()
            os.mkdir('{}\\xml'.format(path))
            print('created directory')
            continue
        else:
            break
    file.write(xml_text)
    file.close()


def form_from_file(file):
    form_b_list = []
    f = open(file, 'r')
    for line in f:
        form_b_list.append(line[0:-2:])
    return form_b_list
