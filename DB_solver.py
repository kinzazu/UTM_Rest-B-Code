import sqlite3


def create_db(db_name: str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE alc_data (name text, code text, form_b text, ready integer, have_form int)''')
    cursor.execute('''CREATE TABLE Marks (form_b text, mark text)''')
    connect.commit()
    connect.close()


def check_columns(db_name: str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('''PRAGMA table_info(alc_data)''')
    result = cursor.fetchall()
    print(result, type(result))


def insert_data(db_name: str, ins_alc_class_list: list):    # Вставляет данные в таблицу SQL
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('''PRAGMA table_info(alc_data)''')
    result = cursor.fetchall()
    if len(result) == 5:
        for data in ins_alc_class_list:
            symbol = (data.alc_form,)

            selec = [data.alc_name, data.alc_code, data.alc_form, 0, None]
            if selec[1] == '500' or selec[1] == '510 ' or selec[1] is None or selec[1] == '520':
                continue
            else:
                cursor.execute('SELECT * FROM alc_data WHERE form_b=?', symbol)
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO alc_data VALUES (?,?,?,?,?)', selec)
                else:
                    '{} already exist'.format(selec[2])
                    continue
            connect.commit()
    else:
        print('DB is old check if "HAVE_FORM" COLUMN EXIST!')


def change_status(db_name: str, formb:str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    sql = """UPDATE alc_data SET ready = 1 WHERE form_b='{}'""".format(formb)
    cursor.execute(sql)
    connect.commit()


def change_have_form(db_name: str, formb:str, have_form): # have_form возращает 1, если на справке есть марки и 0 if no
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    if have_form == 1:
        sql = """UPDATE alc_data SET have_form = 1 WHERE form_b='{}'""".format(formb)
        cursor.execute(sql)
        # после этого нужно вызвать добавление марок в свою таблицу.
    elif have_form == 0:
        sql = """UPDATE alc_data SET have_form = 0 WHERE form_b='{}'""".format(formb)
        cursor.execute(sql)
    connect.commit()


def get_data_db(db_name: str, data_type):    # summary_sql и form_b_sql
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    if data_type == 'form_b_sql':
        sql = """SELECT form_b, code FROM alc_data WHERE ready == 0"""
        cursor.execute(sql)
    elif data_type == 'summary_sql':
        sql = """SELECT count(DISTINCT form_b) FROM alc_data WHERE ready = 0"""
    else:
        print('ты обосрался, кретин, печатать не умеешь?')
        return None
    cursor.execute(sql)
    a = cursor.fetchone()[0]
    return a
