import log_n_save2file
import connectionUTM
from xml_create import compilation_doc as cd
import  DB_solver
from parse import *
import sys
import time


def main_menu(choose):
    if choose == 1:
        list_of_stock = apply_parse('xml/15336.xml')
        class_list = creating_list_of_class(AlcForm,list_of_stock)
        name_of_db = 'green_villa.db' #input('Введите название бд')
        try:
            DB_solver.create_db(name_of_db)
            DB_solver.insert_data(name_of_db, class_list)
        except sqlite3.OperationalError:
            print("!DB is already exist, tring to update data!")
            DB_solver.insert_data(name_of_db, class_list)

        sum_collums = DB_solver.get_data_db(name_of_db, 'summary_sql')
        for i in range(sum_collums):
            print('\n{}/{} :'.format(i, sum_collums))
            form_b =DB_solver.get_data_db(name_of_db, 'form_b_sql')
            print('---- {} ----'.format(form_b))
            xml = cd('020000190211', form_b)
            connectionUTM.send_response('127.0.0.1:4545', xml)
            for i in range(660):
                print('\r{}/660 сек.'.format(i), end='')
                time.sleep(1)
            DB_solver.change_status(name_of_db, form_b)
    elif choose == 4:
        sys.exit(0)


if __name__ == '__main__':
    print('/////___________________________\\\\\\\\\\')
    print('\t Программа для работы с УТМ \n\n \t\n')
    # print('1: получить список справок\n 2:создать файл БД.\n 3:начать запрос справок бд. \n4: выйти\n')
    # a = int(input())
    main_menu(1)
