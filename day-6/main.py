"""
Main script.
"""
import logging
import re
import string
import sys
from dataclasses import dataclass
from enum import Enum, unique
from functools import reduce, total_ordering
from itertools import accumulate, compress
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, NamedTuple, Optional, Set, Tuple


def find_start_of(text: str, distinct_count: int) -> int:
    """
    Solve first part.
    """
    previous = ""
    for idx, letter in enumerate(text):
        if len(previous) < distinct_count - 1:
            previous += letter
            continue

        assert len(previous) <= distinct_count - 1

        current = previous + letter

        if len(set(current)) == distinct_count:
            return idx + 1
        previous = current[1:]

    raise ValueError(f"Expected to find a unique {distinct_count} letter part.")


def first_part(text: str) -> int:
    """
    Solve first part.
    """
    return find_start_of(text=text, distinct_count=4)


def second_part(text: str) -> int:
    """
    Solve second part.
    """
    return find_start_of(text=text, distinct_count=14)


if __name__ == "__main__":
    file_path_arg = sys.argv[1]
    if len(file_path_arg) == 0:
        raise ValueError("Expected a filepath to be passed as argument.")
    file_path = Path(file_path_arg)
    text = file_path.read_text()

    first_part_answer = first_part(text=text)

    print(f"Answer to first part: {first_part_answer}")

    second_part_answer = second_part(text=text)

    print(f"Answer to second part: {second_part_answer}")
