"""
Main script.
"""
import sys
from textwrap import dedent
from enum import Enum, unique
from dataclasses import dataclass
from typing import NamedTuple, Set, Tuple, List
from functools import total_ordering, reduce
import logging
import string
from itertools import accumulate

from pathlib import Path

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"
SAMPLE_DATA_ANSWER = 157


def calculate_priority(token: str) -> int:
    """
    Calculate priority for token.
    """
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase

    if token in lowercase_letters:
        return lowercase_letters.index(token) + 1
    if token in uppercase_letters:
        return uppercase_letters.index(token) + 27
    raise ValueError(f"Expected token {token} to be a lower or uppercase letter.")


def parse_compartment_contents(line: str) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    all_letters = tuple(line)
    all_letters_length = len(all_letters)
    assert all_letters_length == len(line)

    split_index = all_letters_length // 2
    first_compartment = all_letters[0:split_index]
    second_compartment = all_letters[split_index:]
    assert len(first_compartment) == len(second_compartment)
    return first_compartment, second_compartment


def appears_in_both(
    first_compartment: Tuple[str, ...], second_compartment: Tuple[str, ...]
) -> str:
    intersecting = set(first_compartment).intersection(set(second_compartment))
    assert len(intersecting) == 1
    value = intersecting.pop()
    return value


def line_priority(line: str) -> int:
    first_compartment, second_compartment = parse_compartment_contents(line=line)
    token_that_appears_in_both = appears_in_both(first_compartment, second_compartment)
    priority = calculate_priority(token=token_that_appears_in_both)
    return priority


def first_part(text: str):
    assert len(text) > 0

    return sum([line_priority(line) for line in text.splitlines()])


def parse_groups(text: str) -> List[List[str]]:
    lines = text.splitlines()
    groups = [lines[start : start + 3] for start in range(0, len(lines), 3)]
    return groups


def group_priority(group: List[str]) -> int:
    assert len(group) == 3
    logging.info(f"Resolving badge for group with backbacks as such: {group}")
    result = reduce(set.intersection, map(set, group))
    logging.info(f"Badge is {result}")
    assert len(result) == 1
    return calculate_priority(result.pop())


def second_part(text: str):
    groups = parse_groups(text)
    logging.info(f"Found {len(groups)} from read text.")
    result = sum([group_priority(group) for group in groups])
    logging.info(f"Sum of priorities is {result}")

    return result


def test_first_part_with_sample_data():
    assert first_part(SAMPLE_DATA_PATH.read_text()) == 157


def test_second_part_with_sample_data():
    assert second_part(SAMPLE_DATA_PATH.read_text()) == 70


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
