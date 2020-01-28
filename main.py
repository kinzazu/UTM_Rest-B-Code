import sqlite3
import sys
import time
import statistics
import DB_solver
import connectionUTM
import log_n_save2file as lnf
from parse import *
from xml_create import compilation_doc as cd


def timer(timeout):
    stat_for_time = []
    for i in range(int(timeout)):
        inner_start_time = time.time()
        print('\r{}/660 сек.'.format(i), end='')
        time.sleep(1)
        inner_stop_time = time.time() - inner_start_time
        stat_for_time.append(inner_stop_time)
    return statistics.median(stat_for_time)


def main_menu(choose):
    config_path = 'ini/conf.ini'
    config = lnf.Config(config_path)
    if choose == 1:
        try:
            list_of_stock = apply_parse(f'xml/{config.xml_name}')
            class_list = creating_list_of_class(AlcForm, list_of_stock)
        except FileNotFoundError:
            list_of_stock = lnf.form_from_file('test.txt')
            class_list = creating_list_of_class(Only_Form, list_of_stock)

        try:
            DB_solver.create_db(config.DB_name)
        except sqlite3.OperationalError:
            print("!DB is already exist, trying to update data!")
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
            if num % 25 == 0:
                connectionUTM.rest_bcode(parse_response_list(connectionUTM.get_rests_response(config.ip, config.port)), config.DB_name)

    elif choose == 4:
        sys.exit(0)
    elif choose == 2:
        xml = connectionUTM.get_rests_response(config.ip, config.port)        # XML string
        parse_response_rests(xml)


if __name__ == '__main__':
    print('///////___________________________\\\\\\\\\\')
    print('\t Программа для работы с УТМ \n\n \t\n')
    # print('1: получить список справок\n 2:.\n 3:запрос всех необработанх накладных бд. \n4: выйти\n')
    # a = int(input())
    main_menu(1)
