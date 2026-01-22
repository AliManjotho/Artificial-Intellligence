# =========================
# constants.py
# =========================
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Dict

N = 8

# Wall bitmask
WALL_N = 1
WALL_E = 2
WALL_S = 4
WALL_W = 8

DIR_TO_VEC: Dict[str, Tuple[int, int]] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

LEFT_TURN = {"N": "W", "W": "S", "S": "E", "E": "N"}
RIGHT_TURN = {"N": "E", "E": "S", "S": "W", "W": "N"}
BACK_TURN = {"N": "S", "S": "N", "E": "W", "W": "E"}


class Action(Enum):
    FORWARD = auto()
    LEFT = auto()     # turn left then move forward
    RIGHT = auto()    # turn right then move forward
    U_TURN = auto()   # optional (turn around only)


@dataclass(frozen=True)
class Percept:
    front_wall: bool
    left_wall: bool
    right_wall: bool
    position: Tuple[int, int]
    heading: str
