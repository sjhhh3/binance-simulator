import sqlite3
import time
import datetime
import json

conn = sqlite3.connect('./db/database.db')
c = conn.cursor()
COINS = json.loads(open('app/exchange').read())["COINS"]


class Database:
    def __init__(self, username):
        self.username = username
        try:
            c.execute('''SELECT * FROM account LIMIT 1''')
        except:
            self._create_table()

    @staticmethod
    def _create_table():
        c.execute('''
                CREATE TABLE IF NOT EXISTS account
                (uid INTEGER PRIMARY KEY, 
                 reg_timestamp VARCHAR(20) NOT NULL, 
                 reg_datetime DATETIME NOT NULL, 
                 username VARCHAR(40) NOT NULL UNIQUE, 
                 balance FLOAT NOT NULL);
                  ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS orders
                (oid INTEGER PRIMARY KEY, 
                 uid INTEGER NOT NULL, 
                 symbol VARCHAR(10) NOT NULL, 
                 amount FLOAT NOT NULL, 
                 price FLOAT NOT NULL, 
                 operate VARCHAR(5) NOT NULL, 
                 order_time DATETIME NOT NULL, 
                 order_timestamp VARCHAR(20) NOT NULL,
                 FOREIGN KEY (uid) REFERENCES account(uid));
                  ''')

        c.execute(f'''
                CREATE TABLE IF NOT EXISTS balances
                (cid INTEGER PRIMARY KEY,
                 uid INTEGER NOT NULL,
                 {''.join([str(coin)+' FLOAT DEFAULT 0, ' for coin in COINS])}
                 FOREIGN KEY (uid) REFERENCES account(uid));
                  ''')
        conn.commit()

    def _search_user(self):
        c.execute('''SELECT uid FROM account WHERE username = ?''', (self.username,))
        user_id = c.fetchone()
        return user_id[0] if user_id else None

    def create_user(self, init_amount):
        assert 0 < init_amount < 1000000, "Initial amount error"
        if self._search_user():
            print("User Exists")
        else:
            ts = time.time()
            td = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                    INSERT INTO account
                    VALUES (NULL, ?, ?, ?, ?)
                      ''', (ts, td, self.username, init_amount))
            c.execute(f'''
                    INSERT INTO balances (cid, uid)
                    VALUES (NULL, ?)
                      ''', (self._search_user(),))
            conn.commit()
        return self._search_user()

    def get_user_info(self):
        user_id = self._search_user()
        if not user_id:
            user_id = self.create_user(init_amount=10000.00)
        c.execute('''SELECT * FROM account WHERE uid = ?''', (user_id,))
        account_info = c.fetchone()
        return account_info

    def get_coin_amount(self, coin=None):
        assert not coin or coin in COINS, "COIN NAME ERROR"
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        user_id = self._search_user()
        if not user_id:
            user_id = self.create_user(init_amount=10000.00)
        c.execute('''SELECT * FROM balances WHERE uid = ?''', (user_id,))
        balances_info = c.fetchone()
        if not coin:
            return {balances_info.keys()[i]: balances_info[i] for i in range(len(balances_info))}
        else:
            return balances_info[coin]

    def set_coin_amount(self, coin, amount):
        assert 0 < amount < 1000000, "Amount error"
        assert not coin or coin in COINS, "COIN NAME ERROR"
        user_id = self._search_user()
        c.execute(f'''
                  UPDATE balances
                  SET {coin} = {amount}
                  WHERE uid = {user_id}
                  ;''')
        conn.commit()
        return self.get_coin_amount(coin)


if __name__ == "__main__":
    # a = Database('sjhhh3')
    # a.create_user(10000.00)
    # print(a.get_user_info())
    # print(a.get_user_balances())

    b = Database('sjhhh333')
    b.create_user(20000.00)
    print(b.get_user_info())
    print(b.set_coin_amount('BTC', 30.00))
    print(b.get_coin_amount('BTC'))
    Database('sjhhh3').set_coin_amount('BTC', 22.00)