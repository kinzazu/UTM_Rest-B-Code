
import configparser
import os
import datetime


def config_file(file_path, request_attribute):
    config = configparser.ConfigParser()
    config.read(file_path)
    if request_attribute == 'db_name':
        try:
            return config['DB']['name']
        except KeyError:
            print("ошибка в чтении конфиг файла при обращении DB -> Name")
    elif request_attribute == 'ip':
        try:
            return config['TCP']['ip']
        except KeyError:
            print("ошибка в чтении конфиг файла при обращении TCP -> ip")
    elif request_attribute == 'port':
        try:
            return config['TCP']['port']
        except KeyError:
            print("ошибка в чтении конфиг файла при обращении TCP -> ip")
    elif request_attribute == 'xml_file':
        try:
            return config['XML']['name']
        except KeyError:
            print("ошибка в чтении конфиг файла при обращении TCP -> ip")
    else:
        print('OK')
    file.write("\n some_function ")
    file.close()


def save_xml(xml_text, type: int):
    time = datetime.datetime.now()
    print(time)
    if type == 1:
        xml_file_path = 'xml/{}-{}-{} T{}-{}-{}-list.xml'.format(time.year, time.month, time.day,
                                                                 time.hour, time.day, time.second)
    elif type == 2:
        xml_file_path = 'xml/{}-{}-{} T{}-{}-{}-element.xml'.format(time.year, time.month, time.day,
                                                                    time.hour, time.day, time.second)
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
    file.close
