from pathlib import Path
from typing import List, Optional

import main
import pytest

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"


@pytest.mark.parametrize(
    "row,tree_height,answer",
    [
        (
            [0, 3, 7, 3],
            3,
            [1, 1, 0, 0],
        ),
        (
            [0, 3, 3, 3],
            3,
            [1, 1, 0, 0],
        ),
        (
            [0, 2, 3, 3],
            3,
            [1, 1, 1, 0],
        ),
    ],
)
def test_find_visible_for_row_from_tree(
    row: List[int], tree_height: int, answer: List[int]
):
    assert (
        main.find_visible_for_row_from_tree(row=row, tree_height=tree_height) == answer
    )
