"""--- Day 3: Lobby ---"""

import math
from typing import Iterable, NamedTuple, Sequence, TypeAlias

Battery: TypeAlias = int  # joltage
Bank: TypeAlias = Sequence[Battery]


class IndexedBattery(NamedTuple):
    battery: Battery
    index: int


class InvalidBankError(Exception):
    pass


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


def find_first_battery_with_highest_joltage(bank: Bank, /) -> IndexedBattery:
    highest_index: int = 0
    highest_battery: Battery = bank[0]

    index: int
    battery: Battery
    for index, battery in enumerate(bank[1:]):
        if battery < highest_battery:
            continue

        highest_index = index + 1
        highest_battery = battery

    return IndexedBattery(highest_battery, highest_index)


def find_primary_battery(bank: Bank, /) -> IndexedBattery:
    return find_first_battery_with_highest_joltage(bank[:-1])
    # primary_index: int = 0
    # primary_battery: Battery = bank[0]

    # index: int
    # battery: Battery
    # for index, battery in enumerate(bank[1:-1]):
    #     if battery < primary_battery:
    #         continue

    #     primary_index = index
    #     primary_battery = battery

    # return IndexedBattery(primary_battery, primary_index)


def find_secondary_battery(
    bank: Bank, /, *, primary_battery_index: int | None = None
) -> IndexedBattery:
    if primary_battery_index is None:
        primary_battery_index = find_primary_battery(bank).index

    index_offset: int = primary_battery_index + 1
    print("\tPrimary Battery Index:", primary_battery_index)
    print("\tIndex Offset:", index_offset)
    print("\tSub-Bank:", "".join(map(str, bank[index_offset:])))
    secondary_battery: IndexedBattery = find_first_battery_with_highest_joltage(
        bank[index_offset:]
    )

    return IndexedBattery(
        secondary_battery.battery, index_offset + secondary_battery.index
    )

    # secondary_index: int = primary_battery_index + 1
    # secondary_battery: Battery = bank[secondary_index]

    # offset: int
    # battery: Battery
    # for offset, battery in enumerate(bank[secondary_index+1:]):
    #     if battery < secondary_battery:
    #         continue

    #     secondary_index = secondary_index + offset
    #     secondary_battery = battery

    # return IndexedBattery(secondary_battery, secondary_index)


bank: Bank
for bank in read_input():
    primary_battery: IndexedBattery = find_primary_battery(bank)
    secondary_battery: IndexedBattery = find_secondary_battery(
        bank, primary_battery_index=primary_battery.index
    )

    print("Bank:", "".join(map(str, bank)))
    print("Primary:", primary_battery)
    print("Secondary:", secondary_battery)
    break
