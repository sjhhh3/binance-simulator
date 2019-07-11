import os
import time
import datetime
import json
import sqlite3


data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../db/database.db")
exchange_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../db/exchange")
conn = sqlite3.connect(data_path)
c = conn.cursor()
COINS = json.loads(open(exchange_path).read())["COINS"]


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
        init_amount = float(init_amount)
        assert 0 < init_amount < 1000000, "Initial amount error"
        if self._search_user():
            print("User Exists")
            return "Please Try Again"
        else:
            ts = time.time()
            td = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                    INSERT INTO account
                    VALUES (NULL, ?, ?, ?, ?)
                      ''', (ts, td, self.username, init_amount))
            c.execute(f'''
                    INSERT INTO balances (cid, uid, USDT)
                    VALUES (NULL, ?, ?)
                      ''', (self._search_user(), init_amount))
            conn.commit()
            print(f"User Created, Username is {self.username}, Initial Amount is ${init_amount}, User Id is:", end=" ")
        return self._search_user()

    def get_user_info(self):
        user_id = self._search_user()
        if not user_id:
            user_id = self.create_user(init_amount=10000.00)
        c.execute('''SELECT * FROM account WHERE uid = ?''', (user_id,))
        account_info = c.fetchone()
        return account_info

    def get_coin_amount(self, coin=None):
        assert coin in COINS or not coin, "COIN NAME ERROR"
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        user_id = self._search_user()
        if not user_id:
            user_id = self.create_user(init_amount=10000.00)
        c.execute('''SELECT * FROM balances WHERE uid = ?''', (user_id,))
        balances_info = c.fetchone()
        if not coin:
            return {balances_info.keys()[i]: balances_info[i] for i in range(len(balances_info)) if balances_info[i] != 0}
        else:
            return balances_info[coin]

    def set_coin_amount(self, coin, amount):
        if not 0 < amount < 10000000:
            raise ValueError("Amount error")
        if coin and coin not in COINS:
            raise ValueError("COIN NAME ERROR")
        user_id = self._search_user()
        if not user_id:
            user_id = self.create_user(init_amount=10000.00)
        c.execute(f'''
                  UPDATE balances
                  SET {coin} = {amount}
                  WHERE uid = {user_id}
                  ;''')
        conn.commit()
        return self.get_coin_amount(coin)

    def create_order(self, tfsb, ttsb, tfcoin, ttcoin, symbol, amount, price, operate):
        ts = time.time()
        td = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        user_id = self._search_user()
        if not user_id:
            user_id = self.create_user(init_amount=10000.00)
        self.set_coin_amount(tfcoin, tfsb)
        self.set_coin_amount(ttcoin, ttsb)
        print(f"{ttcoin}:{self.get_coin_amount(ttcoin)}, "
              f"{tfcoin}: {self.get_coin_amount(tfcoin)}")
        c.execute(f'''
                  INSERT INTO orders 
                  VALUES (NULL, ?, ?, ?, ?, ?, ?, ?);
                  ''', (user_id, symbol, amount, price, operate, td, ts))
        conn.commit()
        return f"at {td}, created amount of: {amount} {symbol} order at price of {price}."


if __name__ == "__main__":
    pass