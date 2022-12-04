import main
from pathlib import Path

import pytest
from main import Assignment

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"


@pytest.mark.parametrize(
    "first_assignment,second_assignment,result",
    [
        (
            Assignment(start=1, end=5),
            Assignment(start=1, end=5),
            True,
        ),
        (
            Assignment(start=2, end=5),
            Assignment(start=1, end=4),
            False,
        ),
        (
            Assignment(start=2, end=5),
            Assignment(start=3, end=4),
            True,
        ),
    ],
)
def test_assignment_within(
    first_assignment: Assignment, second_assignment: Assignment, result: bool
):
    assert isinstance(first_assignment, Assignment)
    assert isinstance(second_assignment, Assignment)
    assert (second_assignment in first_assignment) == result
    assert (first_assignment.either_contains(second_assignment)) == result
    assert (second_assignment.either_contains(first_assignment)) == result


def test_first_part_with_sample_data():
    assert main.first_part(SAMPLE_DATA_PATH.read_text()) == 2


def test_second_part_with_sample_data():
    assert main.second_part(SAMPLE_DATA_PATH.read_text()) == 4
