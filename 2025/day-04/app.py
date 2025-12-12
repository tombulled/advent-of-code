"""--- Day 4: Printing Department ---"""

from typing import Iterable, Sequence, TypeAlias, TypeVar

T = TypeVar("T")
RawGrid: TypeAlias = Sequence[Sequence[T]]


class Grid[T]:
    _data: Sequence[Sequence[T]]

    def __init__(self, data: Sequence[Sequence[T]], /) -> None:
        self._data = data

    def __getitem__(self, index: int, /) -> Sequence[T]:
        return self._data[index]


def read_input() -> Grid[str]:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        rows: Sequence[Sequence[str]] = [line.strip() for line in file]

        return Grid(rows)

    return rows


d = read_input()
