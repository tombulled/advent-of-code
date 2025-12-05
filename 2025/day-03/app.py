"""--- Day 3: Lobby ---"""

import math
from typing import Iterable, Sequence, TypeAlias, NamedTuple

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

def find_primary_battery(bank: Bank, /) -> IndexedBattery:
    # if len(bank) < 2:
    #     raise InvalidBankError("Bank must have at least two batteries")

    primary_index: int = 0
    primary_battery: Battery = bank[0]
    
    index: int
    battery: Battery
    for index, battery in enumerate(bank[1:-1]):
        if battery < primary_battery:
            continue
            
        primary_index = index
        primary_battery = battery
        
    
    return IndexedBattery(primary_battery, primary_index)
    
# def find_secondary_battery(bank: Bank, /) -> IndexedBattery:
#     # if len(bank) < 2:
#     #     raise InvalidBankError("Bank must have at least two batteries")

#     primary_index: int = 0
#     primary_battery: Battery = bank[0]
    
#     index: int
#     battery: Battery
#     for index, battery in enumerate(bank[1:-1]):
#         if battery < primary_battery:
#             continue
            
#         primary_index = index
#         primary_battery = battery
        
    
#     return IndexedBattery(primary_battery, primary_index)

# bank: Bank
# for bank in read_input():
#     first_digit, first_index = find_first_digit(bank)
    # battery: Battery
    # for battery in bank:
    #     print(battery)
    # break
