"""--- Day 7: Laboratories ---"""

from enum import StrEnum
from typing import (
    Iterable,
    Iterator,
    MutableSequence,
    NamedTuple,
    Sequence,
    Set,
)


class Sprite(StrEnum):
    START = "S"
    EMPTY = "."
    SPLITTER = "^"
    BEAM = "|"


BEAM_EMITTERS: Set[Sprite] = {Sprite.START, Sprite.BEAM}


class Coord(NamedTuple):
    x: int
    y: int


class Cell(NamedTuple):
    coord: Coord
    sprite: Sprite


class Map:
    _data: MutableSequence[MutableSequence[Sprite]]

    def __init__(
        self, data: MutableSequence[MutableSequence[Sprite]], /
    ) -> None:
        self._data = data

    def __getitem__(self, index: int, /) -> MutableSequence[Sprite]:
        return self._data[index]

    def __iter__(self) -> Iterator[Cell]:
        y: int
        for y in range(self.size_y):
            x: int
            for x in range(self.size_x):
                value: T = self.get(x, y)

                yield Cell(Coord(x, y), value)

    @property
    def size_x(self) -> int:
        return len(self._data[0]) if self._data else 0

    @property
    def size_y(self) -> int:
        return len(self._data)

    def get(self, x: int, y: int) -> Sprite:
        return self[y][x]

    def set(self, x: int, y: int, value: Sprite) -> None:
        self[y][x] = value

    def render(self) -> str:
        return "\n".join("".join(row) for row in self._data)

    def print(self) -> None:
        print(self.render())

    def find(self, sprite: Sprite, /) -> Coord:
        cell: Cell
        for cell in self:
            if cell.sprite == sprite:
                return cell.coord


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


def find_beam_emitters(map_: Map, y: int) -> Iterable[Cell]:
    x: int
    sprite: Sprite
    for x, sprite in enumerate(map_[y]):
        if sprite in BEAM_EMITTERS:
            yield Cell(Coord(x, y), sprite)


# def move_da_beam(map_: Map, /) -> None:
#     start_pos: Coord = map_.find(Sprite.START) # should only be done once


EXAMPLE = """\
.......S.......
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

start_pos: Coord = map_.find(Sprite.START)  # should only be done once

y: int
row: Sequence[Sprite]
for y, row in enumerate(map_[start_pos.y + 1 :], start=start_pos.y + 1):
    above_y: int = y - 1
    above_row: Sequence[Sprite] = map_[above_y]

    print("Above  :", f"{''.join(above_row)} ({above_y})")
    print("Current:", f"{''.join(row)} ({y})")

    beam_emitters = find_beam_emitters(map_, above_y)
    # print("Beam Emitters:", list(beam_emitters))

    beam_emitter: Cell
    for beam_emitter in beam_emitters:
        bellow_emitter_pos: Coord = Coord(beam_emitter.coord.x, beam_emitter.coord.y+1)
        bellow_emitter_sprite: Sprite = map_.get(*bellow_emitter_pos)
        bellow_emitter_cell: Cell = Cell(bellow_emitter_pos, bellow_emitter_sprite)

        print("Emitter:", beam_emitter)
        print("Below  :", bellow_emitter_cell)

        match bellow_emitter_sprite:
            case Sprite.EMPTY:
                map_.set(*bellow_emitter_pos, Sprite.BEAM)
            case Sprite.SPLITTER:
                ...
                # put left, put right
            # case *:
            #     # error bro

    print("After  :", f"{''.join(row)} ({y})")
    print()

    break

# for a in map_:
#     print(a)

# while True:
#     ...
