from typing import TypeVar, Callable

import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T")


def try_getenv(key: str, func: Callable[[str], T]) -> T:
    """Tries to get and cast to T an environment variable (loads .env file too).

    Fails if no pair was found with the provided key or if its type isn't the right one"""

    # Tries to get the value
    value: str | None = os.getenv(key)
    if value is None:
        print(f"ERROR: Missing key `{key}` in .env config", file=sys.stderr)
        exit(1)

    # Tries to convert value (str) to T
    try:
        return func(value)
    except:
        print(
            f"ERROR: Wrong key value `{key}` in .env config, expected `{func.__name__}`", file=sys.stderr)
        exit(1)


def get_ttl_hash(minutes: float):
    """Returns the TTL hash of now + N minutes

    Used for LRU cached functions"""

    return round(time.time() / (minutes * 60))
