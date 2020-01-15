import sqlite3


def create_db(db_name: str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    try:
        cursor.execute('''CREATE TABLE stamps (form_b text, mark text)''')
        connect.commit()
    except sqlite3.OperationalError:
        print("Таблица марок уже создана.")
    try:
        cursor.execute('''CREATE TABLE alc_data (name text, code text, form_b text, ready integer, have_form int)''')
        connect.commit()
    except sqlite3.OperationalError:
        add_column(db_name)
        print('Таблица "алкогольная_форма" уже создана.')
    connect.close()


def add_column(db_name):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    try:
        cursor.execute('''ALTER TABLE alc_data ADD COLUMN have_mark INTEGER''')
        connect.commit()
    except sqlite3.OperationalError as e:
        print(e.args[0])
    connect.close()


def check_columns(db_name: str):  # зачем эта функция? пока что она бесполезна 15.01
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('''PRAGMA table_info(alc_data)''')
    result = cursor.fetchall()
    print(result)


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
        print('DB is old check if "HAVE_mark" COLUMN EXIST! \n attempt to add columns')
        try:
            cursor.execute('''ALTER TABLE alc_data ADD COLUMN have_mark INTEGER''')
            connect.commit()
        except sqlite3.OperationalError as e:
            print(e.args[0])
            a = input("ошибка в бд, нужны проверки... нажмать любую клавишу, чтобы выйти")


def change_status(db_name: str, formb: str):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    sql = """UPDATE alc_data SET ready = 1 WHERE form_b='{}'""".format(formb)
    cursor.execute(sql)
    connect.commit()


# have_form return 1, если на справке есть марки и 0 if no
def change_have_form(db_name: str, form_b: str, have_form, mark):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    if have_form == 1:
        insert = [form_b, mark]
        sql = """UPDATE alc_data SET have_mark = 1 WHERE form_b='{}'""".format(form_b)
        cursor.execute(sql)
        cursor.execute("""INSERT INTO stamps VALUES (?,?)""", insert)
    elif have_form == 0:
        sql = """UPDATE alc_data SET have_mark = 0 WHERE form_b='{}'""".format(form_b)
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
