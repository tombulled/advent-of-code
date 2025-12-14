"""--- Day 5: Cafeteria ---"""

from dataclasses import dataclass
from typing import (
    Final,
    Iterable,
    Iterator,
    MutableSequence,
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

    def __gt__(self, rhs: "Range", /) -> bool:
        return self.min > rhs.max

    def __lt__(self, rhs: "Range", /) -> bool:
        return self.max < rhs.min

    def contains(self, value: int, /) -> bool:
        return self.min <= value <= self.max

    def count(self) -> int:
        return self.max - self.min + 1

    def intersects(self, range_: "Range", /) -> bool:
        lhs_intersects_rhs: bool = self.contains(range_.min) or self.contains(
            range_.max
        )
        rhs_intersects_lhs: bool = range_.contains(self.min) or range_.contains(
            self.max
        )

        return lhs_intersects_rhs or rhs_intersects_lhs


class RangeTree:
    _ranges: MutableSequence[Range]

    def __init__(self) -> None:
        self._ranges = []

    def __iter__(self) -> Iterator[Range]:
        yield from self._ranges

    def __len__(self) -> int:
        return len(self._ranges)

    def add(self, range_: Range, /) -> None:
        intersect_index_start: int | None = None
        intersect_index_end: int | None = None

        index: int
        existing_range: Range
        for index, existing_range in enumerate(self):
            if existing_range.intersects(range_):
                if intersect_index_start is None:
                    intersect_index_start = index
            elif intersect_index_start is not None:
                intersect_index_end = index - 1
                break
                
        new_ranges: MutableSequence[Range]
        
        print("Existing Ranges:", self._ranges)
        print("Adding:", range_)

        if intersect_index_end is None:
            intersect_index_end = len(self)
        if intersect_index_start is None:
            if self._ranges and range_ > self._ranges[-1]:
                new_ranges = self._ranges + [range_]
            else:
                new_ranges = [range_] + self._ranges
        else:
            ranges_left: MutableSequence[Range] = self._ranges[
                :intersect_index_start
            ]
            ranges_intersection: MutableSequence[Range] = self._ranges[
                intersect_index_start : intersect_index_end + 1
            ]
            ranges_right: MutableSequence[Range] = self._ranges[
                intersect_index_end + 1 :
            ]
    
            # print(f"Intersection: {intersect_index_start} - {intersect_index_end}")
            print("Left:", ranges_left)
            print("Intersection:", ranges_intersection)
            print("Right:", ranges_right)
            merged_range: Range
            if ranges_intersection:
                merged_range = Range(
                    min=min(range_.min, ranges_intersection[0].min),
                    max=max(range_.max, ranges_intersection[-1].max),
                )
            else:
                merged_range = range_
            print("Merged Intersection:", merged_range)
            
            # self._ranges = ranges_left + [merged_range] + ranges_right
            new_ranges = ranges_left + [merged_range] + ranges_right
        self._ranges = new_ranges
        print("Became:", self._ranges)
        print()

        # ranges_: MutableSequence[Range] = []

        # ranges_to_left = []
        # range_to_insert = None
        # ranges_to_right = []

        # 1. no overlap and existing less than new_range: add existing
        # 2. existing intersects with new range: merge (grow)
        #   new_range = merged range
        #   every range after should be treated as new
        # 3. no overlap and existing greater than [new range]: add existing

        # existing_range: Range
        # for existing_range in self:
        #     previous_range: Range | None = ranges_[-1] if ranges_ else None

        #     # If the new range doesn't overlap the existing range, we can ignore the existing
        #     # range as no merging is required.
        #     if not existing_range.intersects(range_):
        #         ranges_.append(existing_range)
        #         continue

        #     # If the new range intersects with an existing range, grow the existing range
        #     # (if applicable).
        #     if existing_range.contains(range_.min):
        #         existing_range.max = max(existing_range.max, range_.max)

    def get(self, value: int, /) -> Range | None:
        range_: Range
        for range_ in self._ranges:
            if range_.contains(value):
                return range_

        return None

    def contains(self, value: int, /) -> bool:
        return self._get(value) is not None


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


# def merge_ranges(lhs: Range, rhs: Range) -> Range:
#     if not lhs.intersects(rhs):
#         raise Exception  # Temp!

#     return Range(min=min(lhs.min, rhs.min), max=max(lhs.max, rhs.max))


def solve_part_1(database: Database, /) -> int:
    return sum(
        database.is_fresh(ingredient_id)
        for ingredient_id in database.available_ids
    )


# def solve_part_2(database: Database, /) -> int:
#     fresh_ids: MutableSet[int] = set()

#     fresh_id_range: Range
#     for fresh_id_range in database.fresh_id_ranges:
#         fresh_ids.update(fresh_id_range)

#     return fresh_ids # temp


database: Database = read_input()

# ### Part 1 ###
# part_1: int = solve_part_1(database)
# print("Part 1:", part_1)
# assert part_1 == 739

# d = solve_part_2(database)

tree: RangeTree = RangeTree()
# tree._ranges = [
#     Range(1, 1),  # 0
#     Range(2, 2),  # 1
#     Range(3, 3),  # 2
#     Range(4, 4),  # 3
#     Range(5, 5),  # 4
# ]
# 
# tree.add(Range(3, 5))
# tree.add(Range(10, 14))
# tree.add(Range(16, 20))
# tree.add(Range(12, 18))

# tree._ranges = [Range(min=5, max=6)]
# tree.add(Range(min=2, max=3))
# assert tree._ranges == [Range(min=2, max=3), Range(min=5, max=6)]

# tree._ranges = [Range(min=2, max=3)]
# tree.add(Range(min=5, max=6))
# assert tree._ranges == [Range(min=2, max=3), Range(min=5, max=6)]

# print(tree._ranges)

for fresh_range in database.fresh_id_ranges:
    tree.add(fresh_range)
    # input()
    
total = sum(range_.count() for range_ in tree)
# 347316087434620 is too high
# 347124802374240 is too high
