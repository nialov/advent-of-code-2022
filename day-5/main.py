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


class Instruction(NamedTuple):
    move_count: int
    source_stack: int
    destination_stack: int


def parse_marked_crate_line(line: str) -> List[Optional[str]]:

    start_idx = 0
    end_idx = 3
    step = 4
    stop = len(line) + 1

    marked_crates = []
    for i in range(start_idx, stop, step):
        marked_crate = line[i : i + end_idx]
        if marked_crate == "   ":
            marked_crate = None
        marked_crates.append(marked_crate)

    return marked_crates


def parse_input(text: str) -> Tuple[Dict[int, List[str]], List[Instruction]]:
    crates_text, instruction_text = text.split("\n\n")
    crates_text_lines = crates_text.splitlines()
    # crates_keys = list(map(int, crates_text_lines[-1].split(" ")))
    crates_keys_line = crates_text_lines[-1]
    crates_keys = list(map(int, re.findall(r" (\d+) ", crates_keys_line)))

    crates_text_lines_stacks = crates_text_lines[:-1]

    crates_dict = {key: [] for key in crates_keys}

    for line in reversed(crates_text_lines_stacks):

        crates = parse_marked_crate_line(line)
        assert len(crates) == len(crates_dict)
        for marked_crate, key in zip(crates, crates_dict):
            if marked_crate is None:
                continue
            crates_dict[key].append(marked_crate)

    instructions = []
    for instruction_part in instruction_text.splitlines():
        matches = list(map(int, re.findall(r" (\d+)", instruction_part)))
        assert len(matches) == 3
        move_count = matches[0]
        source_stack = matches[1]
        destination_stack = matches[2]
        instruction = Instruction(
            move_count=move_count,
            source_stack=source_stack,
            destination_stack=destination_stack,
        )
        instructions.append(instruction)

    return crates_dict, instructions


def apply_instructions_one_crate_at_a_time(
    crates_dict: Dict[int, List[str]], instructions: List[Instruction]
) -> Dict[int, List[str]]:
    for instruction in instructions:
        crates_to_move = []
        for _ in range(instruction.move_count):
            crates_to_move.append(crates_dict[instruction.source_stack].pop())

        crates_dict[instruction.destination_stack].extend(crates_to_move)
    return crates_dict


def apply_instructions_multiple_crates_at_a_time(
    crates_dict: Dict[int, List[str]], instructions: List[Instruction]
) -> Dict[int, List[str]]:
    for instruction in instructions:
        crates_to_move = []
        for _ in range(instruction.move_count):
            crates_to_move.append(crates_dict[instruction.source_stack].pop())

        crates_dict[instruction.destination_stack].extend(reversed(crates_to_move))
    return crates_dict


def topmost_crate_ids(crates_dict: Dict[int, List[str]]) -> str:
    topmost_crates = [stack[-1] for stack in crates_dict.values()]
    ids = [marked_crate[1:-1] for marked_crate in topmost_crates]
    return "".join(ids)


def first_part(text: str) -> str:
    """
    Solve first part.
    """
    crates_dict, instructions = parse_input(text=text)

    crates_dict_applied = apply_instructions_one_crate_at_a_time(
        crates_dict=crates_dict.copy(), instructions=instructions
    )

    topmost = topmost_crate_ids(crates_dict=crates_dict_applied)
    assert len(topmost) == len(crates_dict)

    return topmost


def second_part(text: str) -> str:
    """
    Solve second part.
    """
    crates_dict, instructions = parse_input(text=text)

    crates_dict_applied = apply_instructions_multiple_crates_at_a_time(
        crates_dict=crates_dict.copy(), instructions=instructions
    )

    topmost = topmost_crate_ids(crates_dict=crates_dict_applied)
    assert len(topmost) == len(crates_dict)

    return topmost


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
