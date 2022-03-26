import sqlite3


class DB:
    def __init__(self):
        self.con = sqlite3.connect('lottery')
        self.cur = self.con.cursor()

    def insert(self, data):
        self.cur.execute(f'''INSERT INTO names (fullname) VALUES ('{data}')''')
        self.con.commit()

    def create_table(self):
        # self.cur.execute('''CREATE TABLE checkscan (scandate date, nonerisa number, erisa number, cafeteria number, operating number''')
        # for testing, I'll create another db with simple text. This way I can test to make sure data is saved after uploaded as a streamlit app
        self.cur.execute('''CREATE TABLE names (fullname text)''')

    def select_all(self):
        data = self.cur.execute('''select * from names''')
        return data
