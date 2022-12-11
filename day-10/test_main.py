from pathlib import Path
from typing import List, Optional

import main
import pytest

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"
PUZZLE_INPUT_PATH = Path(__file__).parent / "puzzle_input.txt"

SMALL_PROGRAM = """
noop
addx 3
addx -5
""".strip()

PART_TWO_SAMPLE_IMAGE = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()


def test_first_part_small_program():
    instructions = [main.parse_line(line=line) for line in SMALL_PROGRAM.splitlines()]
    cycle_states = main.apply_instructions(instructions=instructions)
    assert cycle_states[1] == 1
    assert cycle_states[2] == 1
    assert cycle_states[3] == 4
    assert cycle_states[4] == 4
    assert cycle_states[5] == -1
    assert cycle_states[-1] == -1


def test_part_1_sample_data():
    assert main.first_part(SAMPLE_DATA_PATH.read_text()) == 13140


def test_part_1_puzzle_input():
    assert main.first_part(PUZZLE_INPUT_PATH.read_text()) == 12460


def test_part_2():
    assert main.second_part(SAMPLE_DATA_PATH.read_text()) == PART_TWO_SAMPLE_IMAGE
