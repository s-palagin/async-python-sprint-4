import string

# список запрещенных подсетей
BLACK_LIST: list[str] = [
    '127.0.0.2',
    '192.168.0.1',
]

ALPHABET = string.ascii_letters + string.digits
LINK_LENGTH = 6
