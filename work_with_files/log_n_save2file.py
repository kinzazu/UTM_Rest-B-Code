import datetime
import os

from .path_class import Path2File

# def config_file(file_path, request_attribute):
#     config = configparser.ConfigParser()
#     config.read(file_path)
#     if request_attribute == 'db_name':
#         try:
#             return config['DB_files_old']['name']
#         except KeyError:
#             event = "ошибка в чтении конфиг файла при обращении DB_files_old -> Name"
#             print(event)
#             log_file(event)
#     if request_attribute == 'xml_file':
#         try:
#             return config['XML']['name']
#         except KeyError:
#             event = "ошибка в чтении конфиг файла при обращении XML -> Name"
#             print(event)
#             log_file(event)
#     elif request_attribute == 'ip':
#         try:
#             return config['TCP']['ip']
#         except KeyError:
#             event = "ошибка в чтении конфиг файла при обращении TCP -> ip"
#             print(event)
#             log_file(event)
#     elif request_attribute == 'port':
#         try:
#             return config['TCP']['port']
#         except KeyError:
#             event = "ошибка в чтении конфиг файла при обращении TCP -> port"
#             print(event)
#             log_file(event)
#     elif request_attribute == 'timeout':
#         try:
#             return config['TIME']['timeout']
#         except KeyError:
#             event = "ошибка в чтении конфиг файла при обращении TIME -> timeout"
#             print(event)
#             log_file(event)
#     elif request_attribute == 'fsrar_id':
#         try:
#             return config['UTM']['fsrar_id']
#         except KeyError:
#             event = "ошибка в чтении конфиг файла при обращении UTM -> fsrar_id"
#             print(event)
#             log_file(event)
#     else:
#         print('неправильно указан запрос к .ini файлу!')
path = Path2File()


def create_log_file():
    log_file_path = path.set_path_file(subfolder='Logs', file='{}.log'.format(str(datetime.date.today())))
    while True:
        try:
            file = open(log_file_path, 'x')

        except FileExistsError:
            file = open(log_file_path, 'a')
            break
        except FileNotFoundError:
            os.mkdir(os.path.split(log_file_path)[0])
            print('created directory {}'.format(log_file_path))
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
        xml_file_path = path.set_path_file(subfolder='xml', file='{}-list.xml'.format(time))
    elif type_file == 2:
        xml_file_path = path.set_path_file(subfolder='xml', file='{}-element.xml'.format(time))
    elif type_file == 3:
        xml_file_path = path.set_path_file(subfolder='xml', file='QueryFormBHistory.xml')
    else:
        print("ошибка в типе файла для сохранения xml")
    while True:
        try:

            file = open(xml_file_path, 'w')
        except FileNotFoundError:
            os.mkdir(os.path.split(xml_file_path)[0])
            print('created directory')
            continue
        else:
            break
    file.write(xml_text)
    file.close()


def form_from_file(file):
    form_b_list = []
    try:
        f = open(file, 'r')
        for line in f:
            form_b_list.append(line[0:-2:])
    except FileNotFoundError as e:
        print(e.args[0])
        log_file(e.args[0])
    finally:
        return form_b_list
