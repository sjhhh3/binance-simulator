import sys
import threading
sys.path.append('..')

from db.data import Database
from .API import PublicAPI
from ._log import Log


class Balance:
    def __init__(self, username):
        self.username = username
        self.data = Database(username)
        self.coins = self.data.get_coin_amount()
        self.threadlist = []
        self.total = 0

    def balance_to_usdt_check(self, coin):
        if coin == 'USDT':
            self.total += self.coins['USDT']
            return None
        symbol = coin + 'USDT'
        cur_symbol_info = PublicAPI.get_cur_price(symbol)
        coin_total = float(cur_symbol_info['price']) * self.coins[coin]
        self.total += coin_total
        sys.stdout.write(f"{coin} price: {float(cur_symbol_info['price'])} "
                         f"amount: {self.coins[coin]} total to USDT: {coin_total} \n")

    # O(1) Time complexity, using multi-threads processing, average run time 0.5s
    @Log.run_time_checker
    def total_balance(self):
        for coin in self.coins:
            if coin in ('cid', 'uid'):
                continue
            a = threading.Thread(target=self.balance_to_usdt_check, args=(coin,))
            self.threadlist.append(a)
        for th in self.threadlist:
            th.start()
        for th in self.threadlist:
            th.join()
        Log('balance_log').logger.info(f'INFO LOG: User {self.username}, Total Balance Checked ${self.total}')
        return self.total

    # O(n) Time complexity, average run time (0.5*n)s, n is number of types of coins
    @Log.run_time_checker
    def total_balance_iter(self):
        total = 0
        for coin in self.coins:
            if coin in ('cid', 'uid', 'USDT'):
                continue
            symbol = coin + 'USDT'
            cur_symbol_info = PublicAPI.get_cur_price(symbol)
            coin_total = float(cur_symbol_info['price']) * self.coins[coin]
            total += coin_total
            print(coin, "price:", float(cur_symbol_info['price']),
                  "amount:", self.coins[coin], "total to USDT: ", coin_total)
        total += self.coins.get('USDT', 0)
        return total


if __name__ == "__main__":
    info = f"Total Balance ${Balance('sjhhh3').total_balance()}"
    print(info)
