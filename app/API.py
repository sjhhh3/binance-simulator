import time
import requests
import json
import hashlib
import hmac

import key_config

from urllib.parse import urlencode

BASE_URL = "https://api.binance.com/"


def json_format_decorator(func):
    def func_wrapper():
        return json.dumps(func(), indent=4)

    return func_wrapper


class PublicAPI:
    def __init__(self):
        pass

    def __str__(self):
        return str(dir(PublicAPI))

    @staticmethod
    def ping():
        url = "/api/v1/ping"
        path = f"{BASE_URL}{url}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_server_time():
        url = "/api/v1/time"
        path = f"{BASE_URL}{url}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    # @json_format
    def get_exchange_info():
        url = "/api/v1/exchangeInfo"
        path = f"{BASE_URL}{url}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_depth(symbol, limit=100):
        url = "/api/v1/depth"
        params = {"symbol": symbol, "limit": limit}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_trades(symbol, limit=50):
        url = "/api/v1/trades"
        params = {"symbol": symbol, "limit": limit}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_aggtrades(symbol, fromId=None, startTime=None, endTime=None, limit=50):
        params = locals()
        url = "/api/v1/aggTrades"
        params = {i:params[i] for i in params if params[i]}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_klines(symbol, interval="1m", startTime=None, endTime=None, limit=50):
        params = locals()
        url = "/api/v1/klines"
        params = {i:params[i] for i in params if params[i]}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_avgprice(symbol):
        url = "/api/v3/avgPrice"
        params = {"symbol": symbol}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_24hr(symbol):
        url = "/api/v1/ticker/24hr"
        params = {"symbol": symbol}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_cur_price(symbol):
        url = "/api/v1/ticker/price"
        params = {"symbol": symbol}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()

    @staticmethod
    def get_best_price(symbol):
        url = "/api/v1/ticker/bookTicker"
        params = {"symbol": symbol}
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return requests.get(path, timeout=30, verify=True).json()



class PrivateAPI:
    def __init__(self):
        self.key = key_config.api_key
        self.secret = key_config.secret_key

    def _sign(self, symbol):
        ts = str(int(1000 * time.time()))
        params = {"symbol": symbol, "timestamp": ts, "recvWindow": 5000}
        message = urlencode(params)
        encrypt = self.secret.encode()
        signature = hmac.new(encrypt, msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        params.update({"signature": signature})
        return params

    def _get_with_sign(self, url, symbol):
        url_params = urlencode(self._sign(symbol))
        header = {"X-MBX-APIKEY": self.key}
        url = f"{BASE_URL}{url}?{url_params}"
        return requests.get(url, headers=header, timeout=30, verify=True).json()

    def _get_no_sign(self, url):
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, timeout=30, verify=True).json()

    def get_historical_trades(self, symbol, limit=50, fromId=None):
        url = "/api/v1/historicalTrades"
        params = {"symbol": symbol, "limit": limit}
        if fromId:
            params.update({"fromId": fromId})
        path = f"{BASE_URL}{url}?{urlencode(params)}"
        return self._get_no_sign(path)



a = PublicAPI.get_best_price("CELRUSDT")
print(a)
for i in a:
    print(f"{i}: {a[i]}")