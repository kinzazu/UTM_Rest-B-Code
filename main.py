import sqlite3
import sys
import time

import DB_solver
import connectionUTM
import log_n_save2file as lnf
from parse import *
from xml_create import compilation_doc as cd


def main_menu(choose):
    config_path = 'ini/conf.ini'
    ip = lnf.config_file(config_path, 'ip')
    port = lnf.config_file(config_path, 'port')
    db_name = f"DB/{lnf.config_file(config_path, 'db_name')}"
    timeout = lnf.config_file(config_path, 'timeout')
    if choose == 1:
        list_of_stock = apply_parse('xml/24398.xml')
        class_list = creating_list_of_class(AlcForm, list_of_stock)
        try:
            DB_solver.create_db(db_name)
            DB_solver.insert_data(db_name, class_list)
        except sqlite3.OperationalError:
            print("!DB is already exist, trying to update data!")
            DB_solver.insert_data(db_name, class_list)

        sum_columns = DB_solver.get_data_db(db_name, 'summary_sql')
        for num in range(sum_columns):
            print('\n----{}/{}---- :'.format(num, sum_columns))
            form_b = DB_solver.get_data_db(db_name, 'form_b_sql')
            print('---- {} ----'.format(form_b))
            xml = cd('020000190211', form_b)
            connectionUTM.send_response(ip=ip, port=port, xml_string=xml)
            for i in range(int(timeout)):
                print('\r{}/660 сек.'.format(i), end='')
                time.sleep(1)
            DB_solver.change_status(db_name, form_b)
            if num % 25 == 0:
                connectionUTM.rest_bcode(parse_response_list(connectionUTM.get_rests_response(ip, port)), db_name)

    elif choose == 4:
        sys.exit(0)
    elif choose == 2:
        xml = connectionUTM.get_rests_response(ip, port)        # XML string
        parse_response_rests(xml)


if __name__ == '__main__':
    print('///////___________________________\\\\\\\\\\')
    print('\t Программа для работы с УТМ \n\n \t\n')
    # print('1: получить список справок\n 2:.\n 3:запрос всех необработанх накладных бд. \n4: выйти\n')
    # a = int(input())
    main_menu(1)
