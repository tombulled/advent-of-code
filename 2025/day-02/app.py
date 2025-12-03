import functools
import math
from dataclasses import dataclass
from enum import Enum, auto
from typing import Collection, Final, Iterable, Sequence

ID_SEP: Final[str] = "-"
RANGE_SEPS: Collection[str] = {",", "\n"}


# A tuple would work too... but memory isn't going to use itself
@dataclass
class Range:
    first_id: int
    last_id: int

    def __iter__(self) -> Iterable[int]:
        # First ID and Last ID *inclusive*
        return iter(range(self.first_id, self.last_id + 1))


# I realise you could flip a boolean flag instead... but I like enums, sue me :shrug:
# And besides, what if there were three states? or, heaven forbid, four states??
# Ok, fair enough, we know there's only two.
# ... But what if!
class State(Enum):
    FIRST_ID = auto()
    LAST_ID = auto()


def read_input() -> Iterable[Range]:
    # Big nested functions are the best right?

    file: Iterable[str]
    with open("input", encoding="utf-8") as file:
        state: State | None = None
        first_id: str
        last_id: str

        # I hope I got my exit conditions right...
        while True:
            if state is None:
                # Initialise the state.
                # Is the lack of state... a state? Is nothing something? We may never know
                state = State.FIRST_ID
                first_id = ""
                last_id = ""

            # If you wanted to call this variable `c`, you know where the door is
            character: str = file.read(1)

            match state:
                case State.FIRST_ID:
                    # Woah, a state within a state!
                    if character == ID_SEP:
                        state = State.LAST_ID
                        continue

                    first_id += character
                case State.LAST_ID:
                    if character in RANGE_SEPS:
                        # Validation? Never heard of it.
                        yield Range(int(first_id), int(last_id))

                        # Reset the state
                        state = None

                        continue

                    last_id += character

            # EOF == Ewe Oughta Finish ;)
            if not character:
                break


def int_len(integer: int, /) -> int:
    # Maths refutes the existence of `0`
    if integer == 0:
        return 1

    # Pick that log up off the floor! Do you live in a barn!?
    return math.floor(math.log(integer, 10) + 1)


def int_split(integer: int, /) -> Sequence[int]:
    # I could've modelled the IDs as strings, but where's the fun in that.
    return tuple(
        ((integer // (10**index)) % 10)
        for index in range(int_len(integer) - 1, -1, -1)
    )


def int_join(a: int, b: int, /) -> int:
    # So engrossed in whether we could, we never stopped to think whether we should.
    # But *could* is enough reason for me.
    return a * 10 ** int_len(b) + b


def int_join_all(integers: Sequence[int], /) -> int:
    # I wrote the program, so I no this never happens... I just wouldn't be able to sleep
    # at night otherwise.
    if len(integers) == 0:
        raise ValueError("No integers to join")

    return functools.reduce(int_join, integers)


def validate_id(id_: int, /) -> bool:
    # If its got an off number of digits, then you can't have a sequence repeated twice (must be valid.)
    if int_len(id_) % 2 != 0:
        return True

    digits: Sequence[int] = int_split(id_)
    half_len: int = len(digits) // 2
    first_half: int = int_join_all(digits[:half_len])
    last_half: int = int_join_all(digits[half_len:])

    # Welp, that looks like an invalid ID to me.
    if first_half == last_half:
        return False

    # If it wasn't invalid, then by the laws of deduction and reasoning... it must be valid.
    # Don't you break out the word "quantum" on me. Life's too short to play that game
    return True


invalid_ids_sum: int = 0

# This algorithm is NOT efficient - if I can be asked, I'll come back and reimplement it.
# You should only need to check values that are known to be invalid within the range, rather
# than checking everything.
range_: Range
for range_ in read_input():
    print(range_)
    id_: int
    for id_ in range_:
        if not validate_id(id_):
            print(id_)
            invalid_ids_sum += id_
    print()

print("Part 1:", invalid_ids_sum) # 18596663903 is too high
