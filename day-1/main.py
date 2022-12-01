"""
Main script.
"""
import sys
from textwrap import dedent

from pathlib import Path


def main(file_path: Path):
    text = file_path.read_text()
    assert len(text) > 0

    parts = text.split("\n\n")

    assert len(parts) < len(text.splitlines())

    part_sums = [sum([int(value) for value in part.splitlines()]) for part in parts]

    # Part 1 answer
    most = max(part_sums)
    part_1_answer = f"The elf is carrying a total of {most} calories."

    # Part 2 answer
    sum_of_top_three = sum(sorted(part_sums, reverse=True)[0:3])
    part_2_answer = (
        f"The top three elves are carrying a total of {sum_of_top_three} calories."
    )

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
