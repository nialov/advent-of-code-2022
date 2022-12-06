from pathlib import Path
from typing import List, Optional

import main
import pytest

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"


@pytest.mark.parametrize(
    "line,result",
    [
        (
            "[Z] [M] [P]",
            ["[Z]", "[M]", "[P]"],
        ),
        (
            "    [M]    ",
            [None, "[M]", None],
        ),
        (
            "    [M] [P]",
            [None, "[M]", "[P]"],
        ),
        (
            "        [P]",
            [None, None, "[P]"],
        ),
    ],
)
def test_parse_marked_crate_line(line: str, result: List[Optional[str]]):
    assert main.parse_marked_crate_line(line) == result


def test_parse_input_with_sample_data():
    crates_dict, instructions = main.parse_input(SAMPLE_DATA_PATH.read_text())
    assert isinstance(crates_dict, dict)
    assert isinstance(instructions, list)
    assert len(crates_dict) > 0
    assert len(instructions) > 0
    assert all(key in crates_dict for key in (1, 2, 3))
    stack_contents = [
        ["[Z]", "[N]"],
        ["[M]", "[C]", "[D]"],
        ["[P]"],
    ]
    for stack, assumed_content in zip(crates_dict.values(), stack_contents):
        assert stack == assumed_content


def test_first_part_with_sample_data():
    assert main.first_part(SAMPLE_DATA_PATH.read_text()) == "CMZ"


def test_second_part_with_sample_data():
    assert main.second_part(SAMPLE_DATA_PATH.read_text()) == "MCD"
