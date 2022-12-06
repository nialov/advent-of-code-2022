from pathlib import Path
from typing import List, Optional

import main
import pytest

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"

FIRST_PART_ANSWERS = [7, 5, 6, 10, 11]
SECOND_PART_ANSWERS = [19, 23, 23, 29, 26]


def test_first_part_with_sample_data():
    for line, answer in zip(
        SAMPLE_DATA_PATH.read_text().splitlines(), FIRST_PART_ANSWERS
    ):

        assert main.first_part(line) == answer


def test_second_part_with_sample_data():
    for line, answer in zip(
        SAMPLE_DATA_PATH.read_text().splitlines(), SECOND_PART_ANSWERS
    ):

        assert main.second_part(line) == answer
