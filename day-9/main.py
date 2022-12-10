"""
Main script.
"""
import logging
import math
import re
import string
import sys
from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum, unique
from functools import reduce, total_ordering
from itertools import accumulate, compress
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, NamedTuple, Optional, Set, Tuple, TypedDict, Union


class Point(NamedTuple):
    x: int
    y: int

    def is_adjacent_to(self, other_point: "Point") -> bool:
        return math.dist(self, other_point) < 2

    def touches(self, other_point: "Point") -> bool:
        return math.dist(self, other_point) == 1.0


def determine_azimuth(start_point: Point, end_point: Point) -> float:
    """
    Calculate azimuth of given line.
    """
    start_x = start_point.x
    start_y = start_point.y
    end_x = end_point.x
    end_y = end_point.y
    # start_x = coord_list[0][0]
    # start_y = coord_list[0][1]
    # end_x = coord_list[-1][0]
    # end_y = coord_list[-1][1]
    azimuth = 90 - math.degrees(math.atan2((end_y - start_y), (end_x - start_x)))
    if azimuth < 0:
        azimuth = azimuth + 360
    if azimuth > 360:
        azimuth -= 360
    return azimuth


@unique
class Orientation(Enum):
    N = 0.0
    NE = 45.0
    E = 90.0
    SE = 135.0
    S = 180.0
    SW = 225.0
    W = 270.0
    NW = 315.0

    @classmethod
    def match(cls, value: float):
        for orientation in cls:
            if abs(orientation.value - value) < 0.0001:
                return orientation
        raise ValueError(f"Expected value {value} to match a predefined orientation.")

    @property
    def is_diagonal(self):
        return self in (Orientation.NE, Orientation.SE, Orientation.SW, Orientation.NW)


@unique
class CommandType(Enum):
    RIGHT = "R"
    UP = "U"
    DOWN = "D"
    LEFT = "L"

    @classmethod
    def match(cls, value: str):
        for command_type in cls:
            if value == command_type.value:
                return command_type

        raise ValueError(f"Expected value {value} to match a CommandType.")

    def to_target_point(self, rope_head: Point) -> Point:
        if self is CommandType.UP:
            target_point = Point(rope_head.x, rope_head.y + 1)
        elif self is CommandType.DOWN:
            target_point = Point(rope_head.x, rope_head.y - 1)
        elif self is CommandType.RIGHT:
            target_point = Point(rope_head.x + 1, rope_head.y)
        elif self is CommandType.LEFT:
            target_point = Point(rope_head.x - 1, rope_head.y)
        else:
            raise ValueError(f"Expected self.command_type to be one of CommandType.")
        return target_point


@dataclass
class Rope:
    head: Point
    tail: Point

    @property
    def orientation(self) -> Orientation:
        return Orientation.match(
            determine_azimuth(start_point=self.tail, end_point=self.head)
        )

    def move(self, target_point: Point) -> "Rope":
        movement_orientation = Orientation.match(
            determine_azimuth(start_point=self.head, end_point=target_point)
        )

        new_rope_head = target_point
        if self.tail.is_adjacent_to(new_rope_head):
            # Only update head to target point
            return Rope(head=new_rope_head, tail=self.tail)

        # if movement_orientation.is_diagonal:
        #     import IPython

        #     IPython.embed()

        # x_diff = new_rope_head.x - self.tail.x
        # y_diff = new_rope_head.y - self.tail.y

        # if movement_orientation in (CommandType.UP, CommandType.DOWN):
        if movement_orientation in (Orientation.N, Orientation.S):
            # COlumn after move for tail must be same as head
            new_tail_x = new_rope_head.x
            # Lags one behind
            new_tail_y = (
                (new_rope_head.y - 1)
                if movement_orientation is Orientation.N
                else (new_rope_head.y + 1)
            )
            # new_rope_tail = Point(new_tail_x, new_tail_y)

        # elif movement_orientation in (CommandType.RIGHT, CommandType.LEFT):
        elif movement_orientation in (Orientation.E, Orientation.W):
            # Row after move for tail must be same as head
            new_tail_y = new_rope_head.y
            # Lags one behind
            new_tail_x = (
                (new_rope_head.x - 1)
                if movement_orientation is Orientation.E
                else (new_rope_head.x + 1)
            )
            # new_rope_tail = Point(new_tail_x, new_tail_y)
        elif movement_orientation.is_diagonal:
            if new_rope_head.x == self.tail.x:
                # Same column already as target
                new_tail_x = self.tail.x
                new_tail_y = (
                    (new_rope_head.y - 1)
                    if movement_orientation
                    in (Orientation.N, Orientation.NE, Orientation.NW)
                    else (new_rope_head.y + 1)
                )
            elif new_rope_head.y == self.tail.y:
                # Same row already as target
                new_tail_y = self.tail.y
                new_tail_x = (
                    (new_rope_head.x - 1)
                    if movement_orientation
                    in (Orientation.E, Orientation.NE, Orientation.SE)
                    else (new_rope_head.x + 1)
                )
            elif self.orientation == movement_orientation:
                # else:
                new_tail_y = self.head.y
                new_tail_x = self.head.x
            elif new_rope_head.y != self.tail.y and new_rope_head.x != self.tail.x:
                # Must move diagonally
                # Repeats movement of head

                new_tail_y = self.tail.y + (new_rope_head.y - self.head.y)
                new_tail_x = self.tail.x + (new_rope_head.x - self.head.x)

            else:
                import IPython

                IPython.embed()
            # new_rope_tail =
        else:
            raise ValueError(
                f"Expected movement_orientation {movement_orientation} to be one of Orientation."
            )
        # new_rope_tail = Point()
        new_rope_tail = Point(new_tail_x, new_tail_y)
        return Rope(head=new_rope_head, tail=new_rope_tail)


@dataclass
class Command:
    command_type: CommandType
    move_count: int


def parse_line(line: str) -> Command:
    command_type_str, count_str = line.split(" ")
    return Command(
        command_type=CommandType.match(command_type_str), move_count=int(count_str)
    )


@dataclass
class LongRope:
    segments: List[Rope]

    def move(self, target_point: Point) -> "LongRope":
        moved_segments = []
        for idx, segment in enumerate(self.segments):

            moved_segment = segment.move(target_point=target_point)
            moved_segments.append(moved_segment)
            # if idx == len(self.segments) - 1:
            #     break

            # next_segment = self.segments[idx + 1]
            target_point = moved_segment.tail

        return LongRope(segments=moved_segments)


def first_part(text: str) -> int:
    """
    Solve first part.
    """
    motions = [parse_line(line) for line in text.splitlines()]

    start_point = Point(0, 0)
    rope = Rope(head=start_point, tail=start_point)
    tail_positions = {start_point}

    for motion in motions:
        # Move rope
        for _ in range(motion.move_count):
            rope = rope.move(
                target_point=motion.command_type.to_target_point(rope_head=rope.head)
            )
            tail_positions.add(rope.tail)

    return len(tail_positions)


def second_part(text: str) -> int:
    """
    Solve second part.
    """
    motions = [parse_line(line) for line in text.splitlines()]

    start_point = Point(0, 0)
    long_rope_segments = [Rope(head=start_point, tail=start_point) for _ in range(9)]
    long_rope = LongRope(segments=long_rope_segments)
    tail_positions = {start_point}

    for motion in motions:
        # print(f"Starting motion {motion}")
        # Move rope
        for _ in range(motion.move_count):
            # print(f"Running command {motion.command_type}")
            # print(f"long_rope before: {long_rope}")
            long_rope = long_rope.move(
                target_point=motion.command_type.to_target_point(
                    rope_head=long_rope.segments[0].head
                )
            )
            # print(f"long_rope after: {long_rope}")
            tail_positions.add(long_rope.segments[-1].tail)

    return len(tail_positions)


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
