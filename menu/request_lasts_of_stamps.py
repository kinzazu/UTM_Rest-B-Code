import sqlite3
import time

import work_with_files.log_n_save2file as lnf
from DB import DB_solver
from http_work import connectionUTM
from menu.stopwatch import timer
from parse_files.parse import *
from parse_files.xml_create import compilation_doc as cd
from work_with_files.config_worker import Config


def request_lasts_of_stamps():
    config_path = 'ini/config.ini'
    f = open('conf.ini', 'r')
    for line in f:
        print(line)
    config = Config(config_path)

    try:
        list_of_stock = apply_parse(f'xml/{config.xml_name}')
        class_list = creating_list_of_class(AlcForm, list_of_stock)
    except FileNotFoundError:
        list_of_stock = lnf.form_from_file('test.txt')
        class_list = creating_list_of_class(Only_Form, list_of_stock)

    try:
        DB_solver.create_db(config.DB_name)
    except sqlite3.OperationalError:
        print("!DB_files_old is already exist, trying to update data!")
    finally:
        DB_solver.insert_data(config.DB_name, class_list)
    sum_columns = DB_solver.get_data_db(config.DB_name, 'summary_sql')
    for num in range(sum_columns):
        start_time_column = time.time()
        print('\n----{}/{}---- :'.format(num, sum_columns))
        form_b = DB_solver.get_data_db(config.DB_name, 'form_b_sql')
        print('---- {} ----'.format(form_b))
        xml = cd(config.fsrar_id, form_b)
        connectionUTM.send_response(ip=config.ip, port=config.port, xml_string=xml)
        start_time = time.time()
        median = timer(config.timeout)
        stop_time = time.time() - start_time
        stop_time_column = time.time() - start_time_column
        lnf.log_file(f'Медианное значение между тиками таймаута = {median}')
        lnf.log_file(f'выполнение цикла timeout : {stop_time}')
        lnf.log_file(f'выполнение полного цикла: {stop_time_column}')
        DB_solver.change_status(config.DB_name, form_b)
        # if num % 25 == 0:
        #     connectionUTM.rest_bcode(parse_response_list(connectionUTM.get_rests_response(config.ip, config.port))
        #     , config.DB_name)


if __name__ == '__main__':
    request_lasts_of_stamps()