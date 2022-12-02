"""
Main script.
"""
import sys
from textwrap import dedent
from enum import Enum, unique
from dataclasses import dataclass
from typing import NamedTuple, Set
from functools import total_ordering
import logging

from pathlib import Path


class Code(NamedTuple):
    codes: Set[str]
    score: int


@total_ordering
@unique
class Codes(Enum):
    ROCK = Code({"X", "A"}, 1)
    PAPER = Code({"Y", "B"}, 2)
    SCISSORS = Code({"Z", "C"}, 3)

    def __gt__(self, other):
        if self == Codes.ROCK:
            if other == Codes.SCISSORS:
                return True
        elif self == Codes.PAPER:
            if other == Codes.ROCK:
                return True
        else:
            if other == Codes.PAPER:
                return True
        return False


@unique
class Results(Enum):
    WIN = Code({"Z"}, 6)
    TIE = Code({"Y"}, 3)
    LOSS = Code({"X"}, 0)


def resolve_result(opponent: Codes, own: Codes) -> Results:
    """
    Resolve who wins.
    """
    if own > opponent:
        return Results.WIN
    elif own == opponent:
        return Results.TIE
    else:
        return Results.LOSS


def fix_result(opponent: Codes, wanted_result: Results) -> Codes:
    """
    Resolve what should be picked to match the result as wanted.
    """
    operator_choices = {
        Results.WIN: lambda own, opponent: own > opponent,
        Results.TIE: lambda own, opponent: own == opponent,
        Results.LOSS: lambda own, opponent: own < opponent,
    }
    operator = operator_choices[wanted_result]
    logging.info(f"Choosing operator: {operator}")
    for code in Codes:
        logging.info(f"Comparing {code} with {opponent} with {operator}")
        if operator(code, opponent):
            return code
    raise ValueError(f"Expected operator {operator} to be True for one pair.")


def _match_enum(value, enum_class):
    for code_enum in enum_class:
        if value in code_enum.value.codes:
            return code_enum
    raise ValueError(f"Expected all codes to correspond to {enum_class} enum values.")


def resolve_output(code: str) -> Results:
    return _match_enum(value=code, enum_class=Results)


def resolve_code(code: str) -> Codes:
    return _match_enum(value=code, enum_class=Codes)


def resolve_match(line: str) -> int:
    codes = line.split(" ")
    assert len(codes) == 2
    opponent = resolve_code(codes[0])
    own = resolve_code(codes[1])

    shape_score = own.value.score

    result_score = resolve_result(opponent=opponent, own=own).value.score

    return sum((shape_score, result_score))


def resolve_match_from_result(line: str):
    codes = line.split(" ")
    logging.info(f"Codes are: {codes}")
    assert len(codes) == 2
    opponent = resolve_code(codes[0])
    logging.info(f"Opponent chooses {opponent}")
    result = resolve_output(codes[1])
    logging.info(f"Output should be {result}")

    own_tool = fix_result(opponent, wanted_result=result)

    shape_score = own_tool.value.score
    logging.info(f"Own tool should be {own_tool} which gives {shape_score} points")

    result_score = resolve_result(opponent=opponent, own=own_tool).value.score
    assert result_score == result.value.score

    logging.info(f"Score from the result is {result_score}")

    total_score_for_round = sum((shape_score, result_score))
    logging.info(f"Total score is {total_score_for_round}")
    return total_score_for_round


def main(file_path: Path):
    text = file_path.read_text()
    assert len(text) > 0

    part_1_total_score = sum([resolve_match(line) for line in text.splitlines()])

    part_1_answer = f"The total sum from the strategy in part 1 is {part_1_total_score}"

    part_2_total_score = sum(
        [resolve_match_from_result(line) for line in text.splitlines()]
    )

    part_2_answer = f"The total sum from the strategy in part 2 is {part_2_total_score}"

    return dedent(
        f"""
         {part_1_answer}
         {part_2_answer}
         """
    )


if __name__ == "__main__":
    file_path_arg = sys.argv[1]
    if len(file_path_arg) == 0:
        raise ValueError("Expected a filepath to be passed as argument.")
    file_path = Path(file_path_arg)
    print(main(file_path=file_path))
