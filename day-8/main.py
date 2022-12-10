"""
Main script.
"""
import logging
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


def parse_line(line: str) -> List[int]:
    return [int(char) for char in line]


def parse_text(text: str) -> List[List[int]]:

    return [parse_line(line) for line in text.splitlines()]


def find_visible_for_row(row: List[int]) -> List[int]:
    row_visible = [0 for _ in row]
    current_highest = -1
    for idx, val in enumerate(row):
        if val > current_highest:
            row_visible[idx] += 1
            current_highest = val

    return row_visible


def find_visible_for_row_from_tree(row: List[int], tree_height: int) -> List[int]:
    row_visible = [0 for _ in row]
    for idx, val in enumerate(row):
        # if val < tree_height:
        row_visible[idx] += 1

        if val >= tree_height:
            break

    return row_visible


def first_part(text: str) -> int:
    """
    Solve first part.
    """

    matrix = parse_text(text=text)
    rows_visible: List[List[int]] = []
    for row in matrix:
        row_visible = find_visible_for_row(row)
        row_visible_reversed = list(reversed(find_visible_for_row(list(reversed(row)))))
        row_visible_all = [sum(vals) for vals in zip(row_visible, row_visible_reversed)]
        rows_visible.append(row_visible_all)

    columns = [[row[idx] for row in matrix] for idx in range(len(matrix))]

    columns_visible: List[List[int]] = []
    for column in columns:
        column_visible = find_visible_for_row(column)
        column_visible_reversed = list(
            reversed(find_visible_for_row(list(reversed(column))))
        )
        column_visible_all = [
            sum(vals) for vals in zip(column_visible, column_visible_reversed)
        ]
        columns_visible.append(column_visible_all)

    all_visible_matrix = rows_visible.copy()

    for row_idx, row in enumerate(rows_visible):
        row_from_columns = [column[row_idx] for column in columns_visible]
        for idx in range(len(row)):
            all_visible_matrix[row_idx][idx] += row_from_columns[idx]

    how_many_trees = 0
    for row in all_visible_matrix:
        for value in row:
            if value != 0:
                how_many_trees += 1
    return how_many_trees


def scores_for_arrays(arrays) -> List[List[int]]:
    rows_scores: List[List[int]] = []
    for row in arrays:
        scores = []
        for idx, value in enumerate(row):
            # left to right
            is_last_tree = idx == len(row) - 1
            is_first_tree = idx == 0
            remaining_trees_towards_right = row[idx + 1 :]
            visible_for_tree_towards_right = (
                find_visible_for_row_from_tree(
                    remaining_trees_towards_right, tree_height=value
                )
                if not is_last_tree
                else []
            )
            visible_for_tree_sum_towards_right = sum(
                [visible > 0 for visible in visible_for_tree_towards_right]
            )

            remaining_trees_towards_left = list(reversed(row[:idx]))
            visible_for_tree_towards_left = (
                find_visible_for_row_from_tree(
                    remaining_trees_towards_left, tree_height=value
                )
                if not is_first_tree
                else []
            )
            visible_for_tree_sum_towards_left = sum(
                [visible > 0 for visible in visible_for_tree_towards_left]
            )
            score = (
                visible_for_tree_sum_towards_right * visible_for_tree_sum_towards_left
            )
            scores.append(score)
        rows_scores.append(scores)
    return rows_scores


def second_part(text: str) -> int:
    """
    Solve second part.
    """
    matrix = parse_text(text=text)
    rows_scores = scores_for_arrays(arrays=matrix)
    columns = [[row[idx] for row in matrix] for idx in range(len(matrix))]
    columns_scores = scores_for_arrays(arrays=columns)

    all_scores_matrix = rows_scores.copy()

    for row_idx, row in enumerate(rows_scores):
        row_from_columns = [column[row_idx] for column in columns_scores]
        for idx in range(len(row)):
            all_scores_matrix[row_idx][idx] *= row_from_columns[idx]

    return max([max(row) for row in all_scores_matrix])

    # columns_visible: List[List[int]] = []
    # for column in columns:
    #     column_visible = find_visible_for_row(column)
    #     column_visible_reversed = list(
    #         reversed(find_visible_for_row(list(reversed(column))))
    #     )
    #     column_visible_all = [
    #         sum(vals) for vals in zip(column_visible, column_visible_reversed)
    #     ]
    #     columns_visible.append(column_visible_all)


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
