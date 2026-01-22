# =========================
# constants.py
# =========================

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

# Grid size
N = 8

# Wall bitmask (cell walls)
WALL_N = 1
WALL_E = 2
WALL_S = 4
WALL_W = 8

DIRS = ["N", "E", "S", "W"]
DIR_TO_VEC = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

# Relative directions -> absolute direction index math
LEFT_TURN = {"N": "W", "W": "S", "S": "E", "E": "N"}
RIGHT_TURN = {"N": "E", "E": "S", "S": "W", "W": "N"}
BACK_TURN = {"N": "S", "S": "N", "E": "W", "W": "E"}


class Action(Enum):
    FORWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    U_TURN = auto()  # optional, used for backtracking


@dataclass(frozen=True)
class Percept:
    front_wall: bool
    left_wall: bool
    right_wall: bool
    position: Tuple[int, int]
    heading: str
