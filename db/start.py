import sqlite3
import time
import datetime

conn = sqlite3.connect('./db/database.db')
c = conn.cursor()

class Database:
    def __init__(self, username, init_amount):
        self.username = username
        self.init_amount = init_amount
        try:
            c.execute('''SELECT * FROM account LIMIT 1''')
        except:
            self.create_table()
        finally:
            accounts = c.fetchall()

        if not accounts:
            self.create_user()
        else:
            c.execute('''SELECT * FROM account WHERE username = ?''', (self.username,))
            self.info = c.fetchall()
        print(self.info)

    @staticmethod
    def create_table():
        c.execute('''
                CREATE TABLE IF NOT EXISTS account
                (uid INTEGER PRIMARY KEY, 
                 reg_timestamp VARCHAR(20), 
                 reg_datetime DATETIME, 
                 username VARCHAR(40), 
                 balance FLOAT);
                  ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS orders
                (oid INTEGER PRIMARY KEY, 
                 uid INTEGER, 
                 symbol VARCHAR(10), 
                 amount FLOAT, 
                 price FLOAT, 
                 operate VARCHAR(5), 
                 order_time DATETIME, 
                 order_timestamp VARCHAR(20),
                 FOREIGN KEY (uid) REFERENCES account(uid));
                  ''')
        conn.commit()


    def create_user(self):
        ts = time.time()
        td = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        username = self.username
        balance = self.init_amount
        c.execute('''
                INSERT INTO account
                VALUES (NULL, ?, ?, ?, ?)
                  ''', (ts, td, username, balance))
        conn.commit()

#
# c.execute('''
#         INSERT INTO orders
#         VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
#           ''', (username, "LTCBTC", 100.00, 100.00, "sell", td, ts))
# conn.commit()
# conn.close()

a = Database('sjhhh3', 10000)
