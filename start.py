# import sys
# sys.path.extend(['./app', './db'])
import argparse

from app.order import Order
from app.balance import Balance
from db.data import Database



# Database('sjhhh33').create_user(50000)
# Order('sjhhh333', 'CELR', 'USDT', 3000000)
# print(Balance('sjhhh3').total_balance())
# print(Balance('new_sjhhh33').total_balance())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--balance', '-b', dest='balance', type=str, help='Input username to check balance (Ex: username1)')
    parser.add_argument('--create', '-c', dest='create', nargs='+', help='Create account (Ex: username1 10000)')
    parser.add_argument('--order', '-o', dest='order', nargs='+', help='Create order (Ex: username1 BTC USDT 30000)')

    option = parser.parse_args()
    if (option.create and len(option.create) != 2) or \
       (option.order and len(option.order) != 4):
            raise ValueError("Arguments Error, Please Check Help")

    option_func = {'balance': lambda username: Balance(username).total_balance(),
                   'create': lambda x: Database(x[0]).create_user(x[1]),
                   'order': lambda x: Order(x[0], x[1], x[2], x[3]).market_order()}
    choice = {i: getattr(option, i) for i in option_func if getattr(option, i)}
    func_name = [*choice][0]
    info = option_func[func_name](choice.get(func_name))
    if info:
        print(info)