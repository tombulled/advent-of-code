"""--- Day 3: Lobby ---"""

import functools
import math
from typing import Final, Iterable, NamedTuple, Sequence, TypeAlias

Battery: TypeAlias = int  # joltage
Bank: TypeAlias = Sequence[Battery]

MAX_JOLTAGE: Final[int] = 9


class IndexedBattery(NamedTuple):
    battery: Battery
    index_: int


def parse_bank(bank: str, /) -> Bank:
    return tuple(int(battery) for battery in bank)


def read_input() -> Iterable[Bank]:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        line: str
        for line in file:
            yield parse_bank(line.strip())


def int_len(integer: int, /) -> int:
    if integer == 0:
        return 1

    return math.floor(math.log10(integer) + 1)


def int_join(a: int, b: int, /) -> int:
    return a * 10 ** int_len(b) + b


def int_join_all(integers: Iterable[int], /) -> int:
    return functools.reduce(int_join, integers)


def find_first_battery_with_highest_joltage(bank: Bank, /) -> IndexedBattery:
    highest_index: int = 0
    highest_battery: Battery = bank[0]

    index: int
    battery: Battery
    for index, battery in enumerate(bank[1:]):
        # If this has a lower (or equal!) joltage, ignore it.
        if battery <= highest_battery:
            continue

        # New winner!
        highest_index = index + 1
        highest_battery = battery

        # Nice little optimisation: If the battery has the maximum possible voltage, we can exit early.
        if highest_battery == MAX_JOLTAGE:
            break

    return IndexedBattery(highest_battery, highest_index)


def find_batteries_to_turn_on(bank: Bank, count: int) -> Iterable[IndexedBattery]:
    bank_len: int = len(bank)
    offset: int = 0

    total_batteries_left_to_find: int
    for total_batteries_left_to_find in range(count, 0, -1):
        # Create a subset of the bank, covering the valid search space.
        sub_bank: Bank = bank[offset : bank_len - total_batteries_left_to_find + 1]

        # Find the first battery with the highest joltage within the sub-bank (the search space)
        battery: IndexedBattery = find_first_battery_with_highest_joltage(sub_bank)

        # Calculate the true battery index (taking into account the offset)
        true_battery_index: int = offset + battery.index_

        # Update the index offset now that our search space has shrunk
        offset = true_battery_index + 1

        # Yield the battery with a fixed index
        yield IndexedBattery(battery.battery, true_battery_index)


def calc_max_bank_joltage(bank: Bank, count: int) -> int:
    return int_join_all(
        battery.battery for battery in find_batteries_to_turn_on(bank, count)
    )


def solve_part_1() -> int:
    return sum(calc_max_bank_joltage(bank, 2) for bank in read_input())


def solve_part_2() -> int:
    return sum(calc_max_bank_joltage(bank, 12) for bank in read_input())


def main() -> None:
    ### Part 1 ###
    part_1: int = solve_part_1()
    print("Part 1:", part_1)
    assert part_1 == 17095

    ### Part 2 ###
    part_2: int = solve_part_2()
    print("Part 2:", part_2)
    assert part_2 == 168794698570517


if __name__ == "__main__":
    main()
