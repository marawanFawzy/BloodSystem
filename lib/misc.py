from time import time as _time
from time import gmtime as _gmtime
from time import strftime as _strftime
from random import random as _random
from random import randint as _randint
from base64 import b64encode as _b64encode

# Convert timestamp to string (Egypt Standard Time)

#%a FOR THE DAY
def str_time(time): return _strftime(
    '%a %d/%m %Y, %I:%M %p', _gmtime(time + 7200))

# Return a random positive integer


def random(): return _randint(0, 999999)


def obscure(text):
    if len(text) > 8:
        return ('*' * (len(text) - 4)) + (text[-4:])
    if len(text) > 6:
        return ('*' * (len(text) - 3)) + (text[-3:])
    if len(text) > 4:
        return ('*' * (len(text) - 2)) + (text[-2:])
    return text


def generateID():
    token = bin(int(_time() ** 1.5 / _random()))[2:].zfill(48)
    token = bytes(int(token[i: i + 8], 2) for i in range(0, 48, 8))
    return _b64encode(token, b'2y').decode()


def time():
    return int(_time())


def date():
    return _strftime('%a %d/%m/%Y', _gmtime(_time() + 7200))


def datetime():
    return _strftime('%a %d %b %Y, %H:%M', _gmtime(_time() + 7200))
