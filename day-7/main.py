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


class DirectoryName(str):
    pass


@dataclass
class CdCmd:
    target: DirectoryName
    value: str = "cd"


@dataclass
class LsCmd:
    value: str = "ls"


@dataclass
class File:
    name: str
    size: int


def parse_line(line: str):
    if line.startswith("$"):
        if line[2:4] == CdCmd.value:
            # cmd = cd_cmd
            # cmd.target =
            return CdCmd(target=DirectoryName(line[5:]))
        else:
            return LsCmd()

    if line.startswith("dir"):
        name = line[4:]
        return DirectoryName(name)

    # Only file left
    size, *name_parts = line.split(" ")
    name = " ".join(name_parts)
    size_int = int(size)
    return File(name=name, size=size_int)


class Directory(dict):
    def __init__(self):
        super(dict, self).__init__()
        self.files = {}

    def __repr__(self) -> str:
        repr = super().__repr__()
        return f"{repr} ({self.file_size()})"

    def file_size(self) -> int:
        total_size = 0
        current_dir_file_size = sum(self.files.values())
        if len(self) == 0:
            return current_dir_file_size

        total_size += current_dir_file_size
        for value in self.values():
            total_size += value.file_size()

        return total_size

    # name:str
    # parent: "Directory"


class RootDirectory(Directory):
    pass


def update_filetree(
    file_tree: Directory,
    location: List[DirectoryName],
    addition: Union[DirectoryName, File],
) -> Tuple[Directory, List[DirectoryName]]:

    # print(location)
    # print(filetree)

    if len(location) == 0:
        if isinstance(addition, DirectoryName):
            # New directory
            if addition not in file_tree:
                file_tree[addition] = Directory()
            return file_tree, location
        elif isinstance(addition, File):
            file_tree.files[addition.name] = addition.size
            return file_tree, location
    next_directory_name = location.pop(0)
    # Recurse deeper
    next_filetree = file_tree[next_directory_name]
    updated_filetree, location = update_filetree(
        file_tree=next_filetree, location=location, addition=addition
    )
    file_tree[next_directory_name] = updated_filetree

    return file_tree, location


def search_lower_than_value(value: int, file_tree: Directory, collection: List[int]):

    file_tree_size = file_tree.file_size()
    if file_tree_size < value:
        # print(dict(file_tree_size=file_tree_size, file_tree=file_tree))
        collection.append(file_tree_size)
        # return collection

    for key in file_tree:
        next_file_tree = file_tree[key]
        collection = search_lower_than_value(
            value=value, file_tree=next_file_tree, collection=collection
        )

    return collection


def parse_file_tree(text: str) -> Directory:
    file_tree = Directory()
    shell_location = []

    for line in text.splitlines():
        parsed = parse_line(line)

        if isinstance(parsed, CdCmd):
            # Change directory
            target = parsed.target
            if target == "..":
                shell_location.pop()
            elif target == "/":
                # Initialization of root
                if target not in file_tree:
                    file_tree[target] = RootDirectory()

                shell_location = [target]
            else:
                file_tree, _ = update_filetree(
                    file_tree=file_tree, location=shell_location.copy(), addition=target
                )
                shell_location.append(target)
        elif isinstance(parsed, (DirectoryName, File)):
            file_tree, _ = update_filetree(
                file_tree=file_tree, location=shell_location.copy(), addition=parsed
            )
    return file_tree


def first_part(text: str):
    """
    Solve first part.
    """
    file_tree = parse_file_tree(text=text)
    return sum(
        search_lower_than_value(value=100000, file_tree=file_tree, collection=[])
    )


def find_smallest_possible(value: int, file_tree: Directory, collection: List[int]):
    file_tree_size = file_tree.file_size()
    if file_tree_size >= value:
        collection.append(file_tree_size)
        # return collection

    for key in file_tree:
        next_file_tree = file_tree[key]
        collection = find_smallest_possible(
            value=value, file_tree=next_file_tree, collection=collection
        )

    return collection


def second_part(text: str) -> int:
    """
    Solve second part.
    """
    file_tree = parse_file_tree(text=text)
    total_disk_space = 70000000
    needed_disk_space = 30000000
    used_space = file_tree.file_size()
    unused_space = total_disk_space - used_space
    space_to_remove = needed_disk_space - unused_space

    collection = find_smallest_possible(
        value=space_to_remove, file_tree=file_tree, collection=[]
    )

    return min(collection)


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
