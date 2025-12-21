"""--- Day 7: Laboratories ---"""

from enum import StrEnum
from typing import Iterable, MutableSequence


class Sprite(StrEnum):
    START = "S"
    EMPTY = "."
    SPLITTER = "^"
    BEAM = "|"


class Map:
    _data: MutableSequence[MutableSequence[Sprite]]

    def __init__(
        self, data: MutableSequence[MutableSequence[Sprite]], /
    ) -> None:
        self._data = data

    def render(self) -> str:
        return "\n".join("".join(row) for row in self._data)

    def print(self) -> None:
        print(self.render())


def parse_input(input_: str, /) -> Map:
    rows: MutableSequence[MutableSequence[str]] = [
        [Sprite(character) for character in line]
        for line in input_.splitlines()
    ]

    return Map(rows)


def read_input() -> Map:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return parse_input(file.read())


EXAMPLE = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

# map_: Map = read_input()
map_: Map = parse_input(EXAMPLE)
