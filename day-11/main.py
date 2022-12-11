"""
Main script.
"""
import logging
import math
import operator
import re
import string
import sys
from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum, unique
from functools import cached_property, lru_cache, reduce, total_ordering
from itertools import accumulate, compress
from pathlib import Path
from textwrap import dedent
from typing import (
    Callable,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    TypedDict,
    Union,
)


@unique
class OperationType(Enum):
    ADDITION = "+"
    MULTIPLICATION = "*"


class Operation(NamedTuple):
    operation_type: OperationType
    target: Optional[int]


class Monkey(NamedTuple):
    id: int
    # items: List[int]
    operation: Operation
    divisible_value: int
    true_throw_target: int
    false_throw_target: int

    def party(
        self,
        items: List[int],
        no_division: bool = False,
        lcm: int = 0,
    ) -> Iterator[Tuple[int, int]]:

        for item in items:
            yield self.inspect(item=item, no_division=no_division, lcm=lcm)

    def inspect(
        self,
        item: int,
        lcm: int,
        no_division: bool = False,
    ):
        if self.operation.operation_type is OperationType.ADDITION:
            worry = item + (
                item if self.operation.target is None else self.operation.target
            )
        else:
            # multiplication
            # math required...
            target_maybe = self.operation.target
            multiplier = target_maybe if target_maybe is not None else item
            if not no_division:
                # Part 1
                worry = item * multiplier
            else:
                # Part 2
                if (
                    multiplier % self.divisible_value == 0
                    or item % self.divisible_value == 0
                ):
                    return self.true_throw_target, (item * multiplier) % lcm
                else:
                    a = item % self.divisible_value
                    true_result = item * multiplier
                    hack_result = a * multiplier
                    assert (true_result % self.divisible_value) == (
                        hack_result % self.divisible_value
                    )
                    return self.false_throw_target, (true_result % lcm)

        # worry = self.operation(item)
        if not no_division:
            worry /= 3
        worry = math.floor(worry)
        if worry % self.divisible_value == 0:
            return self.true_throw_target, worry
        else:
            return self.false_throw_target, worry


@dataclass
class MonkeyParty:
    monkeys: List[Monkey]
    monkey_items: List[List[int]]
    inspection_counts: Dict[int, int] = field(default_factory=dict)

    @cached_property
    def lcm(self):
        """
        Did not figure this lcm one out myself...
        """
        lcm = math.lcm(*[monkey.divisible_value for monkey in self.monkeys])
        return lcm

    def __getitem__(self, key: int) -> Monkey:
        for monkey in self.monkeys:
            if monkey.id == key:
                return monkey
        raise KeyError(f"Expected key to be an id of one of the monkeys.")

    def __repr__(self) -> str:
        with_keys = {monkey.id: monkey for monkey in self.monkeys}
        return str(with_keys)

    def round(self, no_division: bool = False):
        for idx, monkey in enumerate(self.monkeys):
            # print(f"Monkey {idx} {Monkey} is partying.")
            items = self.monkey_items[idx]
            # print(f"Items: {items}")
            for target, item in monkey.party(
                items=items, no_division=no_division, lcm=self.lcm
            ):
                # Throw the item
                self.monkey_items[target].append(item)
                # print(f"Threw {item} to {target} from monkey: {monkey}")
                self.inspection_counts[idx] = self.inspection_counts.get(idx, 0) + 1
            self.monkey_items[idx] = []


# def parse_operation(line: str) -> Callable[[int], int]:
def parse_operation(line: str) -> Operation:
    if OperationType.ADDITION.value in line:
        # addition
        operation_type = OperationType.ADDITION
    elif OperationType.MULTIPLICATION.value in line:
        # multiplication
        operation_type = OperationType.MULTIPLICATION
    else:
        raise ValueError("Expected addition or multiplication only.")

    target = re.findall(pattern=r"[\*\+] (.*)", string=line)[0]
    assert isinstance(target, str)
    # if target_match is None:
    #     raise ValueError(f"Expected to match target in line: {line}")

    try:
        resolved_target = int(target)
    except ValueError:
        resolved_target = None

    # func = lambda val: operation(val, (target if not target_is_old else val))
    # return lambda val: operation(val, (target if not target_is_old else val))
    return Operation(operation_type=operation_type, target=resolved_target)

    # return lru_cache()(func)


def parse_monkey_and_items(monkey_text: str) -> Tuple[Monkey, List[int]]:
    lines = monkey_text.splitlines()
    monkey_id = int(re.findall(pattern=r" (\d+):", string=lines[0])[0])
    items = list(map(int, re.findall(pattern=r"(\d+)", string=lines[1])))
    operation = parse_operation(lines[2])
    divisible_value = int(re.findall(pattern=r" (\d+)", string=lines[3])[0])
    true_throw_target = int(re.findall(pattern=r" (\d+)", string=lines[4])[0])
    false_throw_target = int(re.findall(pattern=r" (\d+)", string=lines[5])[0])

    return (
        Monkey(
            id=monkey_id,
            operation=operation,
            divisible_value=divisible_value,
            true_throw_target=true_throw_target,
            false_throw_target=false_throw_target,
        ),
        items,
    )


def first_part(text: str) -> int:
    """
    Solve first part.
    """
    monkeys, all_items = [], []

    for monkey_text in text.split("\n\n"):
        monkey, monkey_items = parse_monkey_and_items(monkey_text=monkey_text)
        monkeys.append(monkey)
        all_items.append(monkey_items)
    monkey_party = MonkeyParty(monkeys=monkeys, monkey_items=all_items)

    for _ in range(20):
        monkey_party.round()

    # Order is ascending by default
    sorted_counts = sorted(monkey_party.inspection_counts.values())

    return sorted_counts[-2] * sorted_counts[-1]


def second_part(text: str) -> int:
    """
    Solve second part.
    """
    monkeys, all_items = [], []

    for monkey_text in text.split("\n\n"):
        monkey, monkey_items = parse_monkey_and_items(monkey_text=monkey_text)
        monkeys.append(monkey)
        all_items.append(monkey_items)
    monkey_party = MonkeyParty(monkeys=monkeys, monkey_items=all_items)

    for _ in range(10000):
        monkey_party.round(no_division=True)

    print(monkey_party.inspection_counts)
    # Order is ascending by default
    sorted_counts = sorted(monkey_party.inspection_counts.values())

    print(sorted_counts)
    return sorted_counts[-2] * sorted_counts[-1]


if __name__ == "__main__":
    file_path_arg = sys.argv[1]
    if len(file_path_arg) == 0:
        raise ValueError("Expected a filepath to be passed as argument.")
    file_path = Path(file_path_arg)
    text = file_path.read_text()

    first_part_answer = first_part(text=text)

    print(f"Answer to first part: {first_part_answer}")

    second_part_answer = second_part(text=text)

    print(f"Answer to second part:\n\n{second_part_answer}")
