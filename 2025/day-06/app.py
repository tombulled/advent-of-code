"""--- Day 6: Trash Compactor ---"""

import functools
import operator
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, MutableSequence, Protocol, Sequence


class OperatorFunc(Protocol):
    def __call__(self, a: int, b: int, /) -> int: ...


class ProblemSolver(Protocol):
    def __call__(self, problem: "Problem", /) -> int: ...


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
    operands: Sequence[str]


def parse_numbers(numbers_lines: Sequence[str], /) -> Sequence[Sequence[str]]:
    all_numbers: MutableSequence[Sequence[str]] = []

    numbers: MutableSequence[str] = []

    column: Sequence[str]
    for column in zip(*numbers_lines):
        is_separator: bool = all(character == " " for character in column)

        if is_separator:
            all_numbers.append(numbers)
            numbers = []
            continue

        if not numbers:
            numbers = [""] * len(column)

        operand_index: int
        character: str
        for operand_index, character in enumerate(column):
            numbers[operand_index] += character

    if numbers:
        all_numbers.append(numbers)

    return list(zip(*all_numbers))


def parse_input(input_: str, /) -> Iterable[Problem]:
    numbers_lines: Sequence[str]
    symbols_line: str
    *numbers_lines, symbols_line = input_.splitlines()

    numbers: Sequence[Sequence[str]] = parse_numbers(numbers_lines)
    symbols: Sequence[str] = symbols_line.split()

    operands: Sequence[str]
    symbol: str
    for *operands, symbol in zip(*numbers, symbols):
        operator: Operator = Operator.from_symbol(symbol)

        yield Problem(operator, operands)


def read_input() -> Iterable[Problem]:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        return parse_input(file.read())


def solve_problem_part_1(problem: Problem, /) -> int:
    operands: Sequence[int] = [int(operand) for operand in problem.operands]

    return functools.reduce(problem.operator.func, operands)


def solve_problem_part_2(problem: Problem, /) -> int:
    # Flip the order of the operands (right-to-left baby!)
    operands_rtl: Sequence[str] = [
        operand[::-1] for operand in problem.operands
    ]

    # Read the operands as columns
    operands: Sequence[int] = [
        int("".join(column)) for column in zip(*operands_rtl)
    ]

    return functools.reduce(problem.operator.func, operands)


def calculate_grand_total(
    problems: Sequence[Problem], solver: ProblemSolver
) -> int:
    return sum(solver(problem) for problem in problems)


def solve_part_1(problems: Sequence[Problem], /) -> int:
    return calculate_grand_total(problems, solve_problem_part_1)


def solve_part_2(problems: Sequence[Problem], /) -> int:
    return calculate_grand_total(problems, solve_problem_part_2)


def main() -> None:
    problems: Sequence[Problem] = list(read_input())

    ### Part 1 ###
    part_1: int = solve_part_1(problems)
    print("Part 1:", part_1)
    assert part_1 == 5227286044585

    ## Part 2 ###
    part_2: int = solve_part_2(problems)
    print("Part 2:", part_2)
    assert part_2 == 10227753257799


if __name__ == "__main__":
    main()
