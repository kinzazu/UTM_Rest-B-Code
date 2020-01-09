import sqlite3


def create_db(db_name: str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE alc_data (name text, code text, form_b text, ready integer)''')
    connect.commit()
    connect.close()


def insert_data(db_name: str, ins_alc_class_list: list):  # если повторить, на заполненных значениях, то данные задублируются, аккуратне!
    connect = sqlite3.connect(db_name)                    # сделал условие, вроде избавил его от дублирования.
    cursor = connect.cursor()
    for data in ins_alc_class_list:
        symbol = (data.alc_form,)

        selec = [data.alc_name, data.alc_code, data.alc_form, 0]
        if selec[1] == '500' or selec[1] == '510 ' or selec[1] is None:
            continue
        else:
            cursor.execute('SELECT * FROM alc_data WHERE form_b=?', symbol)
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO alc_data VALUES (?,?,?,?)', selec)
            else:
                '{} already exist'.format(selec[2])
                continue
        connect.commit()


def change_status(db_name: str, formb:str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    sql = """UPDATE alc_data SET ready = 1 WHERE form_b='{}'""".format(formb)
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
