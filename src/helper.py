from typing import TypeVar, Callable
import os
import sys

from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T")

def try_getenv(key: str, func: Callable[[str], T]) -> T:
    value: str | None = os.getenv(key)
    if value is None:
        print(f"ERROR: Missing key `{key}` in .env config", file=sys.stderr)
        exit(1)

    try:
        return func(value)
    except:
        print(
            f"ERROR: Wrong key value `{key}` in .env config, expected `{func.__name__}`", file=sys.stderr)
        exit(1)
