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
        return iter(range(self.first_id, self.last_id))


# I realise you could flip a boolean flag instead... but I like enums, sue me :shrug:
# And besides, what if there were three states? or, heaven forbid, four states??
# Ok, fair enough, we know there's only two.
# ... But what if!
class State(Enum):
    FIRST_ID = auto()
    LAST_ID = auto()


def read_input() -> Iterable[Range]:
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
    if integer == 0:
        return 1

    return math.floor(math.log(abs(integer), 10) + 1)


def int_split(integer: int, /) -> Sequence[int]:
    return tuple(
        ((integer // (10**index)) % 10)
        for index in range(int_len(integer) - 1, -1, -1)
    )


# range_: Range
# for range_ in read_input():
#     print(range_)
#     id_: int
#     for id_ in range_:
#         digits: Sequence[int] = int_split(id_)
#         print(id_, digits)
#         break
#     break

i = 82915517
d = int_split(i)
