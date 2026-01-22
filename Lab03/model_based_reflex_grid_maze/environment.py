# =========================
# environment.py
# =========================

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

from constants import (
    N,
    WALL_N, WALL_E, WALL_S, WALL_W,
    DIR_TO_VEC, LEFT_TURN, RIGHT_TURN, BACK_TURN,
    Action, Percept,
)

def _in_bounds(r: int, c: int, n: int) -> bool:
    return 0 <= r < n and 0 <= c < n

def _wall_bit_for_dir(d: str) -> int:
    return {"N": WALL_N, "E": WALL_E, "S": WALL_S, "W": WALL_W}[d]

def _opposite_dir(d: str) -> str:
    return {"N": "S", "S": "N", "E": "W", "W": "E"}[d]


@dataclass
class RobotState:
    r: int
    c: int
    heading: str  # "N","E","S","W"


class MazeEnv:
    """
    Known-maze environment for an 8x8 grid.
    walls[r][c] is a bitmask with WALL_N/E/S/W.
    """
    def __init__(
        self,
        walls: List[List[int]],
        start: Tuple[int, int] = (0, 0),
        goal: Tuple[int, int] = (7, 7),
        start_heading: str = "E",
    ):
        if len(walls) != N or any(len(row) != N for row in walls):
            raise ValueError(f"walls must be {N}x{N}")
        self.walls = walls
        self.start = start
        self.goal = goal
        self.robot = RobotState(start[0], start[1], start_heading)
        self.steps = 0

        # Basic validation: ensure outer boundaries have walls
        self._validate_outer_walls()

    def reset(self) -> None:
        self.robot = RobotState(self.start[0], self.start[1], self.robot.heading)
        self.steps = 0

    def is_terminal(self) -> bool:
        return (self.robot.r, self.robot.c) == self.goal

    def _has_wall(self, r: int, c: int, direction: str) -> bool:
        bit = _wall_bit_for_dir(direction)
        return (self.walls[r][c] & bit) != 0

    def _validate_outer_walls(self) -> None:
        # Top row must have N walls; bottom row must have S walls; etc.
        for c in range(N):
            if not self._has_wall(0, c, "N"):
                raise ValueError("Top boundary missing a NORTH wall")
            if not self._has_wall(N - 1, c, "S"):
                raise ValueError("Bottom boundary missing a SOUTH wall")
        for r in range(N):
            if not self._has_wall(r, 0, "W"):
                raise ValueError("Left boundary missing a WEST wall")
            if not self._has_wall(r, N - 1, "E"):
                raise ValueError("Right boundary missing an EAST wall")

    def get_percept(self) -> Percept:
        r, c, h = self.robot.r, self.robot.c, self.robot.heading
        front = self._has_wall(r, c, h)
        left = self._has_wall(r, c, LEFT_TURN[h])
        right = self._has_wall(r, c, RIGHT_TURN[h])
        return Percept(
            front_wall=front,
            left_wall=left,
            right_wall=right,
            position=(r, c),
            heading=h,
        )

    def step(self, action: Action) -> None:
        """
        Applies an action (turn or forward). FORWARD is blocked by a wall.
        """
        if action is None:
            # treat as NO-OP
            return
    
        self.steps += 1
        r, c, h = self.robot.r, self.robot.c, self.robot.heading

        if action == Action.TURN_LEFT:
            self.robot.heading = LEFT_TURN[h]
            return
        if action == Action.TURN_RIGHT:
            self.robot.heading = RIGHT_TURN[h]
            return
        if action == Action.U_TURN:
            self.robot.heading = BACK_TURN[h]
            return

        if action == Action.FORWARD:
            if self._has_wall(r, c, h):
                # blocked: stay in place
                return
            dr, dc = DIR_TO_VEC[h]
            nr, nc = r + dr, c + dc
            # in a well-formed maze, bounds should be protected by walls;
            # still, guard.
            if 0 <= nr < N and 0 <= nc < N:
                self.robot.r, self.robot.c = nr, nc
            return

        raise ValueError(f"Unknown action: {action}")
