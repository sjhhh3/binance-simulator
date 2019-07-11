# binance-simulator ![version](https://img.shields.io/badge/Version-1.0-blue.svg)
For those who always wait-and-see the cryptocurrency market, want to join in but worry about the loss and secure, a simple script has been developed by me. Based on Binance API and grab the current price of each cryptocurrency existing on Binance Market, simulate a local trading platform. No more loss and secure worry since it creates your own sqlite3 database locally. Every behavior will be stored at "logs" folder for user to check.
## Preview
![binance](https://user-images.githubusercontent.com/13906239/61072348-15c96500-a3e1-11e9-8851-61cc4a5b800d.JPG)

## Requirements
* Python3
* Standard library

## Running
Just download and unzip the file, using the command-line to run start.py file and pass the arguments.
* ### Create User  (--create, -c)
(Arguments: username, initiate USDT amount)
```
python start.py --create user1 10000
# Create user1 and initiate the account USDT amount to $100,00
```

* ### Create Order (--order, -o)
(Arguments: username, buy cryptocurrency symbol, spend cryptocurrency symbol, amount)
```
python start.py --order user1 BTC USDT 0.1
# Create a market order that spending USDT to buy 0.1 BTC
```

* ### Check Balance (--balance, -b)
(Argument: username)
```
python start.py --balance user1
# Check user1's balance of each cryptocurrency possessed, and total estimated balance converting to USDT
``` 
## Todo
* Spend the maximum amount to buy this cryptocurrency
* Balance fluctuations check
* Python shell running script with menu
* ......

## Authors

* **Duxxi** - [Duxxi](https://github.com/sjhhh3)

## License
![licence](https://img.shields.io/badge/license-MIT-green.svg)

Code released under the [MIT License](https://opensource.org/licenses/MIT).

---
