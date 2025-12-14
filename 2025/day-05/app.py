"""--- Day 5: Cafeteria ---"""

from dataclasses import dataclass
from typing import (
    Final,
    Iterable,
    Iterator,
    MutableSequence,
    MutableSet,
    Sequence,
)

RANGE_SEP: Final[str] = "-"
SECTION_SEP: Final[str] = "\n\n"


@dataclass
class Range:
    min: int
    max: int

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.min, self.max + 1))

    def contains(self, value: int, /) -> bool:
        return self.min <= value <= self.max


@dataclass
class Database:
    fresh_id_ranges: Sequence[Range]
    available_ids: Sequence[int]

    def is_fresh(self, id_: int, /) -> bool:
        fresh_id_range: Range
        for fresh_id_range in self.fresh_id_ranges:
            if fresh_id_range.contains(id_):
                return True

        return False


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


def solve_part_1(database: Database, /) -> int:
    return sum(
        database.is_fresh(ingredient_id)
        for ingredient_id in database.available_ids
    )


def solve_part_2(database: Database, /) -> int:
    fresh_ids: MutableSet[int] = set()

    fresh_id_range: Range
    for fresh_id_range in database.fresh_id_ranges:
        fresh_ids.update(fresh_id_range)
        
    return fresh_ids # temp


database: Database = read_input()

# ### Part 1 ###
# part_1: int = solve_part_1(database)
# print("Part 1:", part_1)
# assert part_1 == 739

d = solve_part_2(database)
