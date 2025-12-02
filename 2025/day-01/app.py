from dataclasses import dataclass
from typing import Final, Iterable
from enum import Enum


DIAL_MAX: Final[int] = 99
DIAL_START: Final[int] = 50


class Direction(str, Enum):
    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"<{self.name}>"

    LEFT = "L"
    RIGHT = "R"


@dataclass
class Rotation:
    direction: Direction
    distance: int


class InvalidRotationError(Exception):
    pass


def parse_rotation(rotation: str, /) -> Rotation:
    if len(rotation) < 2:
        raise InvalidRotationError(
            f"Rotation {rotation!r} missing direction and/or distance"
        )

    raw_direction: str = rotation[0]
    raw_distance: str = rotation[1:]

    direction: Direction
    try:
        direction = Direction(raw_direction)
    except ValueError:
        raise InvalidRotationError(f"{raw_direction!r} is not a valid direction")

    distance: int
    try:
        distance = int(raw_distance)
    except ValueError:
        raise InvalidRotationError(f"{raw_distance!r} is not a valid distance")

    return Rotation(
        direction=direction,
        distance=distance,
    )


def read_input() -> Iterable[Rotation]:
    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        line: str
        for line in file:
            yield parse_rotation(line)


def apply_rotation(position: int, rotation: Rotation) -> int:
    multiplier: int = -1 if rotation.direction is Direction.LEFT else 1

    return (position + multiplier * rotation.distance) % (DIAL_MAX + 1)


position: int = DIAL_START
zeroth_position_counter: int = 0

rotation: Rotation
for rotation in read_input():
    position = apply_rotation(position, rotation)

    if position == 0:
        zeroth_position_counter += 1

print("Total Times at Position 0:", zeroth_position_counter)
assert zeroth_position_counter == 1076
