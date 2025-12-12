"""--- Day 4: Printing Department ---"""

from enum import Enum
from typing import (
    Iterable,
    Iterator,
    MutableSequence,
    NamedTuple,
    Sequence,
    Tuple,
)


class CellType(str, Enum):
    EMPTY = "."
    PAPER_ROLL = "@"


class Coord(NamedTuple):
    x: int
    y: int


class Cell[T](NamedTuple):
    coord: Coord
    value: T


class Grid[T]:
    _data: Sequence[Sequence[T]]

    def __init__(self, data: Sequence[Sequence[T]], /) -> None:
        self._data = data

    # def __repr__(self) -> str:
    #     return f"{type(self).__name__}(size={self.size})"

    def __getitem__(self, index: int, /) -> Sequence[T]:
        return self._data[index]

    def __iter__(self) -> Iterator[Cell[T]]:
        y: int
        for y in range(self.size_y):
            x: int
            for x in range(self.size_x):
                value: T = self.get(x, y)

                yield Cell(Coord(x, y), value)

    def get(self, x: int, y: int) -> T:
        return self[y][x]

    def contains(self, x: int, y: int) -> bool:
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def get_surrounding(self, x: int, y: int) -> Sequence[Cell]:
        neighbours: MutableSequence[Cell] = []

        neighbour_x: int
        for neighbour_x in range(x - 1, x + 2, 1):
            neighbour_y: int
            for neighbour_y in range(y - 1, y + 2, 1):
                if not self.contains(neighbour_x, neighbour_y) or (
                    neighbour_x == x and neighbour_y == y
                ):
                    continue

                cell: Cell[T] = Cell(
                    Coord(neighbour_x, neighbour_y),
                    self.get(neighbour_x, neighbour_y),
                )

                neighbours.append(cell)

        return neighbours

    @property
    def size_x(self) -> int:
        return len(self._data[0]) if self._data else 0

    @property
    def size_y(self) -> int:
        return len(self._data)

    @property
    def size(self) -> Tuple[int, int]:
        return (self.size_x, self.size_y)


def read_input() -> Grid[str]:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        rows: Sequence[Sequence[str]] = [line.strip() for line in file]

        return Grid(rows)


def solve_part_1() -> int:
    grid: Grid[str] = read_input()
    total_rolls_accessible_by_forklift: int = 0

    coord: Coord
    value: str
    for coord, value in grid:
        cell_type: CellType = CellType(value)

        if cell_type != CellType.PAPER_ROLL:
            continue

        total_adjacent_rolls: int = sum(
            CellType(value) == CellType.PAPER_ROLL
            for _, value in grid.get_surrounding(*coord)
        )

        if total_adjacent_rolls < 4:
            total_rolls_accessible_by_forklift += 1

    return total_rolls_accessible_by_forklift
    

### Part 1 ###
part_1: int = solve_part_1()
print("Part 1:", part_1)
assert part_1 == 1540
