"""--- Day 5: Cafeteria ---"""

from dataclasses import dataclass
from typing import (
    Final,
    Iterable,
    Iterator,
    MutableSequence,
    Sequence,
    Tuple,
)

RANGE_SEP: Final[str] = "-"
SECTION_SEP: Final[str] = "\n\n"


@dataclass
class Range:
    min: int
    max: int

    def __gt__(self, rhs: "Range", /) -> bool:
        return self.min > rhs.max

    def __lt__(self, rhs: "Range", /) -> bool:
        return self.max < rhs.min

    def contains(self, value: int, /) -> bool:
        return self.min <= value <= self.max

    def count(self) -> int:
        return self.max - self.min + 1


class RangeTree:
    _ranges: MutableSequence[Range]

    def __init__(self, ranges: Iterable[Range] | None = None, /) -> None:
        self._ranges = []

        if ranges is not None:
            for range_ in ranges:
                self.add(range_)

    def __iter__(self) -> Iterator[Range]:
        yield from self._ranges

    def _get_insertion_coords(self, range_: Range, /) -> Tuple[int, int]:
        # 1. Insert at the beginning
        if not self._ranges or range_ < self._ranges[0]:
            return (0,) * 2

        # 2. Insert at the end
        if range_ > self._ranges[-1]:
            return (len(self._ranges),) * 2

        index_lt: int | None = None
        index_gt: int | None = None

        index: int
        existing_range: Range
        for index, existing_range in enumerate(self):
            if existing_range < range_:
                index_lt = index
            elif existing_range > range_:
                index_gt = index
                break

        index_start: int = index_lt + 1 if index_lt is not None else 0
        index_end: int = index_gt if index_gt is not None else len(self._ranges)

        # 3. Insert in the middle (might span either end)
        return (index_start, index_end)

    def add(self, range_: Range, /) -> None:
        insert_start: int
        insert_end: int
        insert_start, insert_end = self._get_insertion_coords(range_)

        if insert_start == insert_end:
            self._ranges.insert(insert_start, range_)
            return

        intersection: Sequence[Range] = self._ranges[insert_start:insert_end]

        merged_range = Range(
            min=min(range_.min, intersection[0].min),
            max=max(range_.max, intersection[-1].max),
        )

        self._ranges[insert_start:insert_end] = [merged_range]

    def contains(self, value: int, /) -> bool:
        range_: Range
        for range_ in self._ranges:
            if range_.contains(value):
                return True

        return False


@dataclass
class Database:
    fresh_id_ranges: Sequence[Range]
    available_ids: Sequence[int]


def parse_range(range_: str) -> Range:
    min_: str
    max_: str
    min_, max_ = range_.split(RANGE_SEP)

    return Range(
        min=int(min_),
        max=int(max_),
    )


def parse_input(input_: str, /) -> Database:
    raw_fresh_id_ranges: str
    raw_available_ids: str
    raw_fresh_id_ranges, raw_available_ids = input_.split(SECTION_SEP)

    fresh_id_ranges: MutableSequence[Range] = [
        parse_range(raw_fresh_id_range)
        for raw_fresh_id_range in raw_fresh_id_ranges.splitlines()
    ]
    available_ids: MutableSequence[Range] = [
        int(raw_available_id)
        for raw_available_id in raw_available_ids.splitlines()
    ]

    return Database(
        fresh_id_ranges=fresh_id_ranges,
        available_ids=available_ids,
    )


def read_input() -> ...:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return parse_input(file.read())


def solve_part_1(database: Database, tree: RangeTree) -> int:
    return sum(
        tree.contains(ingredient_id) for ingredient_id in database.available_ids
    )


def solve_part_2(database: Database, tree: RangeTree) -> int:
    for fresh_range in database.fresh_id_ranges:
        tree.add(fresh_range)

    return sum(range_.count() for range_ in tree)


database: Database = read_input()
tree: RangeTree = RangeTree(database.fresh_id_ranges)

### Part 1 ###
part_1: int = solve_part_1(database, tree)
print("Part 1:", part_1)
assert part_1 == 739

### Part 2 ###
part_2: int = solve_part_2(database, tree)
print("Part 2:", part_2)
assert part_2 == 344486348901788
