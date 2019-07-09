from API import PublicAPI
from db.data import Database
from _log import Log


class Order:
    def __init__(self, username, bto, bfrom, amount):
        self.trade_to_coin = bto
        self.trade_from_coin = bfrom
        self.amount = amount
        self.data = Database(username)
        self.ori_from_coin_amount = self.data.get_coin_amount(bfrom)
        self.ori_to_coin_amount = self.data.get_coin_amount(bto)
        self.symbol = self.trade_to_coin + self.trade_from_coin
        # Only Market Order For Now
        info = self.market_order()
        Log('order_log').logger.info(f'INFO LOG: User:{username} {info}')

    @Log.run_time_checker
    def market_order(self):
        cur_symbol_info = PublicAPI.get_cur_price(self.symbol)
        if 'msg' in cur_symbol_info:
            raise ValueError('Symbol Error')
        cur_price = float(cur_symbol_info["price"])
        max_buy_amount = self.ori_from_coin_amount / cur_price
        if self.amount > max_buy_amount:
            raise ValueError(f"Insufficient balance, maximum amount for your balance to buy "
                             f"{self.trade_to_coin} is {max_buy_amount}.")
        from_set_balance = self.ori_from_coin_amount - self.amount*cur_price
        to_set_balance = self.ori_to_coin_amount + self.amount
        order_res = self.data.create_order(from_set_balance,
                                       to_set_balance,
                                       self.trade_from_coin,
                                       self.trade_to_coin,
                                       self.symbol,
                                       self.amount,
                                       cur_price,
                                       'market')
        return order_res


if __name__ == "__main__":
    o1 = Order('sjhhh3', 'BNB', 'BTC', 0.1)
