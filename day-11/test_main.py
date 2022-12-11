from pathlib import Path
from typing import List, Optional

import main
import pytest

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"
PUZZLE_INPUT_PATH = Path(__file__).parent / "puzzle_input.txt"


def test_sample_data_round_one():
    monkeys, all_items = [], []

    for monkey_text in SAMPLE_DATA_PATH.read_text().split("\n\n"):
        monkey, monkey_items = main.parse_monkey_and_items(monkey_text=monkey_text)
        monkeys.append(monkey)
        all_items.append(monkey_items)
    monkey_party = main.MonkeyParty(monkeys=monkeys, monkey_items=all_items)
    monkey_party.round()
    assert monkey_party.monkey_items == [
        [20, 23, 27, 26],
        [2080, 25, 167, 207, 401, 1046],
        [],
        [],
    ]
    monkey_party.round()
    assert monkey_party.monkey_items == [
        [695, 10, 71, 135, 350],
        [43, 49, 58, 55, 362],
        [],
        [],
    ]
    monkey_party.round()
    assert monkey_party.monkey_items == [
        [16, 18, 21, 20, 122],
        [1468, 22, 150, 286, 739],
        [],
        [],
    ]


def test_part_1_sample_data():
    assert main.first_part(SAMPLE_DATA_PATH.read_text()) == 10605


def test_part_1_puzzle_input():
    assert main.first_part(PUZZLE_INPUT_PATH.read_text()) == 50830


def test_part_2():
    assert main.second_part(SAMPLE_DATA_PATH.read_text()) == 2713310158
