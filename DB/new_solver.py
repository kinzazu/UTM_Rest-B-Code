import sqlite3

class DB:
    def __init__(self,file_name):
        self.file_name= file_name
        self.connect = sqlite3.connect(self.file_name)
        self.c = self.connect.cursor()
        self.c.execute()

    def create_table(self,table_name, column_parameters):
        self.c.execute(f'''CREATE TABLE {table_name} ({column_parameters})''')

        print()

    def insert_data(self, ):
        self.c.execute()
        self.commit()

    def get_data(self):
        self.c.execute()
        self.commit()

    def commit(self):
        self.connect.commit()
    def close(self):
        self.connect.close()


class TableDB(DB):
    def __init__(self, config_name, columns=None):
        self.name = config_name
        if columns is None:
            columns = ''
        self.columns = columns
        # self.

    def add_column(self):
