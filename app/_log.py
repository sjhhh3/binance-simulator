import time
import logging


class Log:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler(f'logs/{name}')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    @staticmethod
    def run_time_checker(func):
        start = time.time()
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            print(f"Run Time: {time.time() - start}")
            return res
        return wrapper
