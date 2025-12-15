"""--- Day 6: Trash Compactor ---"""

import functools
import operator
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol, Sequence


class OperatorFunc(Protocol):
    def __call__(self, a: int, b: int, /) -> int: ...


class Operator(Enum):
    symbol: str
    func: OperatorFunc

    ADD = ("+", operator.add)
    MULTIPLY = ("*", operator.mul)

    def __init__(self, symbol: str, func: OperatorFunc) -> None:
        self.symbol = symbol
        self.func = func

    @classmethod
    def from_symbol(cls, symbol: str, /) -> "Operator":
        member: Operator
        for member in cls:
            if member.symbol == symbol:
                return member

        raise ValueError(f"No such operator with symbol {symbol!r}")


@dataclass
class Problem:
    operator: Operator
    operands: Sequence[int]

    def solve(self) -> int:
        return functools.reduce(self.operator.func, self.operands)


def parse_input(input_: str, /) -> Iterable[Problem]:
    rows: Sequence[Sequence[str]] = [
        line.split() for line in input_.splitlines()
    ]

    numbers: Sequence[str]
    symbol: str
    for *numbers, symbol in zip(*rows):
        operator: Operator = Operator.from_symbol(symbol)
        operands: Sequence[int] = [int(number) for number in numbers]

        yield Problem(operator, operands)


def read_input() -> Iterable[Problem]:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return parse_input(file.read())


def solve_part_1() -> int:
    return sum(problem.solve() for problem in read_input())


### Part 1 ###
part_1: int = solve_part_1()
print("Part 1:", part_1)
assert part_1 == 5227286044585
