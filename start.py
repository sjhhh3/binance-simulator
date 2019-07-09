from app.order import Order
from app.balance import Balance
from data import Database

# Database('sjhhh33').create_user(50000)
# Order('sjhhh333', 'CELR', 'USDT', 3000000)
print(Balance('sjhhh333').total_balance())
# print(Balance('new_sjhhh33').total_balance())
