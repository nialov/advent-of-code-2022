from pathlib import Path
from typing import List, Optional

import main
import pytest
from main import CommandType, Point, Rope

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"


@pytest.mark.parametrize(
    "target_points,expected_tail_positions",
    [
        (
            [
                # CommandType.RIGHT,
                main.Point(1, 0),
                # CommandType.RIGHT,
                main.Point(2, 0),
                # CommandType.RIGHT,
                main.Point(3, 0),
                # CommandType.UP,
                main.Point(3, 1),
                # CommandType.UP,
                main.Point(3, 2),
            ],
            [
                main.Point(0, 0),
                main.Point(1, 0),
                main.Point(2, 0),
                main.Point(2, 0),
                main.Point(3, 1),
            ],
        )
    ],
)
def test_rope_move(
    target_points: List[Point],
    expected_tail_positions: List[Point],
):
    start_point = Point(0, 0)
    rope = Rope(head=start_point, tail=start_point)

    for target_point, expected_tail_position in zip(
        target_points, expected_tail_positions
    ):
        rope = rope.move(target_point=target_point)
        assert rope.tail == expected_tail_position


def test_part_1():
    assert main.first_part(SAMPLE_DATA_PATH.read_text()) == 13


def test_part_2():
    assert main.second_part(SAMPLE_DATA_PATH.read_text()) == 1
