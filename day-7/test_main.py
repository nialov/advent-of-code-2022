from pathlib import Path
from typing import List, Optional

import main
import pytest

SAMPLE_DATA_PATH = Path(__file__).parent / "sample_data.txt"


def test_update_filetree():

    filetree = main.Directory()
    b_filetree = main.Directory()
    b_filetree["c"] = main.Directory()
    filetree["a"] = b_filetree

    location = ["a", "c"]

    new_node_name = "d"

    result, empty_location = main.update_filetree(
        filetree=filetree, location=location.copy(), name=new_node_name
    )
    print(result)

    assert "d" in result["a"]["c"]
    assert "d" not in result["a"]
    assert len(empty_location) == 0


def test_update_filetree_2():
    filetree = main.Directory()
    b_filetree = main.Directory()
    b_filetree["c"] = main.Directory()
    filetree["a"] = b_filetree

    new_node_name = "d"

    result, empty_location = main.update_filetree(
        filetree=filetree, location=["a"], name=new_node_name
    )

    assert "d" in result["a"]
    assert "d" not in result["a"]["c"]
    assert "c" in result["a"]
    assert len(empty_location) == 0


# def test_first_part_with_sample_data():
#     assert main.first_part(SAMPLE_DATA_PATH.read_text())


# def test_second_part_with_sample_data():
#     for line, answer in zip(
#         SAMPLE_DATA_PATH.read_text().splitlines(), SECOND_PART_ANSWERS
#     ):

#         assert main.second_part(line) == answer
