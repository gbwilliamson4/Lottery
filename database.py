import sqlite3
import pandas as pd

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

    def get_players(self):
        query = '''SELECT PlayerID, PlayerName FROM PLAYERS WHERE ACTIVE = 1'''
        data = self.cur.execute(query)
        return data

    def store_guesses(self, player_list, scan_date):
        for player in player_list:
            query = f'''INSERT INTO PlayerGuesses (ScanDate, PlayerID, NonErisa, Erisa, Cafeteria, Operating) VALUES ('{scan_date}', {player.playerID}, {player.nonerisa}, {player.erisa}, {player.cafeteria}, {player.operating})'''
            self.cur.execute(query)
            self.con.commit()

    def store_winning_nums(self, winning_nums, scan_date):
        nonerisa = winning_nums.nonerisa
        erisa = winning_nums.erisa
        cafeteria = winning_nums.cafeteria
        operating = winning_nums.operating
        query = f'''INSERT INTO checkscan (ScanDate, NonErisa, Erisa, Cafeteria, Operating) VALUES ('{scan_date}', {nonerisa}, {erisa}, {cafeteria}, {operating})'''
        self.cur.execute(query)
        self.con.commit()

    def log_winner(self, playerID, gamemode, scan_date):
        query = f"INSERT INTO Winners (PlayerID, GamemodeID, WinDate) VALUES ({playerID}, {gamemode}, '{scan_date}')"
        self.cur.execute(query)
        self.con.commit()

    def date_testing(self, date):
        query = f'''INSERT INTO datetesting (mydate) VALUES ('{date}')'''
        self.cur.execute(query)
        self.con.commit()
        print(query)

    def date_testing2(self):
        query = f'''select max(mydate) as date from datetesting'''
        result = pd.read_sql(query, self.con)
        return result

    def date_testing3(self):
        query = f'''select ScanDate, nonerisa, erisa, cafeteria, operating from checkscan'''
        result = pd.read_sql(query, self.con)
        return result

    def inserting_dummy_data(self, df, table):
        df.to_sql(f'{table}', self.con, if_exists='append', index=False)
