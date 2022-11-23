from secrets import choice

from core.config import ALPHABET


def get_short_link(length: int) -> str:
    return "".join(choice(ALPHABET) for _ in range(length))
