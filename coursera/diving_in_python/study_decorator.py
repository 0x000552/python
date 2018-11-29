"""
Some project's doc string...

"""

import time
import sys
import os.path


def logit(log_file):
    def dec_logger(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(log_file, 'a+') as f:
                f.write(f'{time.strftime("%c"):10s}: {func.__qualname__:10s} -> {result}\n')
            return result

        return wrapper

    return dec_logger


def _main():
    if len(sys.argv) != 2:
        log_file = 'log.log'
        pkg_file_name = os.path.basename(__file__) if __file__ else 'study_decorator.py'
        print(f'\033[91musage: {pkg_file_name} log_file\033[0m\n'
              'current log_file = {log_file}\n\n')
    else:
        log_file = sys.argv[1]

    @logit(log_file)  # greet = logit(log_file).__call__(greet)
    def greet(name='<NAME>'):
        return f'Hello, {name}'

    def __read_log():
        with open(log_file, 'r') as f:
            print(f'\n==== {f.name} ====\n\n{f.read()}\n')

    print(greet())
    __read_log()
    print(greet('Bob'))
    __read_log()


if __name__ == '__main__':
     _main()
