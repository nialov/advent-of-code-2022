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


@unique
class InstructionTypes(Enum):
    NOOP = ("noop", 1)
    ADDX = ("addx", 2)

    @classmethod
    def match(cls, value: str) -> "InstructionTypes":
        for instruction_type in cls:
            if value == instruction_type.value[0]:
                return instruction_type

        raise ValueError(f"Expected value {value} to match a InstructionTypes.")


class Instruction(NamedTuple):
    instruction_type: InstructionTypes
    value: int = 0


def parse_line(line: str) -> Instruction:
    if line == InstructionTypes.NOOP.value[0]:
        return Instruction(instruction_type=InstructionTypes.NOOP)

    instruction_type_str, value = line.split(" ")
    return Instruction(
        instruction_type=InstructionTypes.match(instruction_type_str), value=int(value)
    )


def apply_instructions(
    instructions: List[Instruction], starting_x: int = 1
) -> List[int]:
    cycle_states = [starting_x]
    x = starting_x
    for instruction in instructions:
        if instruction.instruction_type is InstructionTypes.NOOP:
            cycle_states.append(x)
        else:
            additions = [x for _ in range(instruction.instruction_type.value[1] - 1)]
            x += instruction.value
            cycle_states.extend([*additions, x])
    return cycle_states


def first_part(text: str) -> int:
    """
    Solve first part.
    """

    instructions = [parse_line(line=line) for line in text.splitlines()]

    cycle_states = apply_instructions(instructions=instructions)

    cycle_indexes = (20, 60, 100, 140, 180, 220)

    cycle_values = []
    for idx in cycle_indexes:
        x_state = cycle_states[idx - 1]
        # print(cycle_states[idx - 1 : idx + 2])
        # cycle_sum += x_state * idx
        cycle_value = x_state * idx
        cycle_values.append(cycle_value)
        # print(idx, x_state, cycle_value)

    return sum(cycle_values)


def second_part(text: str) -> str:
    """
    Solve second part.
    """
    instructions = [parse_line(line=line) for line in text.splitlines()]

    cycle_states = apply_instructions(instructions=instructions)

    rows = []
    row = ""
    for idx, state in enumerate(cycle_states):
        row_idx = idx % 40
        if row_idx == 0 and idx != 0:
            rows.append(row)
            print(f"Finished row: {row}")
            row = ""

        draw_indexes = range(state - 1, state + 2)
        if row_idx in draw_indexes:
            row += "#"
        else:
            row += "."
    return "\n".join(rows)


if __name__ == "__main__":
    file_path_arg = sys.argv[1]
    if len(file_path_arg) == 0:
        raise ValueError("Expected a filepath to be passed as argument.")
    file_path = Path(file_path_arg)
    text = file_path.read_text()

    first_part_answer = first_part(text=text)

    print(f"Answer to first part: {first_part_answer}")

    second_part_answer = second_part(text=text)

    print(f"Answer to second part:\n\n{second_part_answer}")
