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
from itertools import accumulate, compress

from pathlib import Path


class Assignment(NamedTuple):
    start: int
    end: int

    def __contains__(self: "Assignment", other: "Assignment") -> bool:
        return (self.start <= other.start) and (self.end >= other.end)

    def either_contains(self, other: "Assignment") -> bool:
        return self in other or other in self

    def intersects(self: "Assignment", other: "Assignment") -> bool:
        start_intersects = self.start >= other.start and self.start <= other.end
        end_intersects = self.end <= other.end and self.end >= other.start
        return start_intersects or end_intersects

    def either_intersects(self: "Assignment", other: "Assignment") -> bool:
        return self.intersects(other) or other.intersects(self)


def parse_line(line: str) -> Tuple[Assignment, Assignment]:
    """
    Parse line to starts and ends of both pairs.
    """
    first_assignment, second_assignment = line.split(",")
    first_assignment_start, first_assignment_end = list(
        map(int, first_assignment.split("-"))
    )
    second_assignment_start, second_assignment_end = list(
        map(int, second_assignment.split("-"))
    )
    return Assignment(first_assignment_start, first_assignment_end), Assignment(
        second_assignment_start,
        second_assignment_end,
    )


def first_part(text: str) -> int:
    """
    Solve first part.
    """
    assignment_pairs = [parse_line(line) for line in text.splitlines()]

    either_contains_other = [
        Assignment.either_contains(first, second) for first, second in assignment_pairs
    ]
    return sum(either_contains_other)


def second_part(text: str) -> int:
    """
    Solve second part.
    """
    assignment_pairs = [parse_line(line) for line in text.splitlines()]
    logging.info(f"All pairs: {assignment_pairs}")

    intersecting = [
        Assignment.either_intersects(first, second)
        for first, second in assignment_pairs
    ]
    logging.info(
        f"Intersecting pairs: {list(compress(assignment_pairs, intersecting))}"
    )
    return sum(intersecting)


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
