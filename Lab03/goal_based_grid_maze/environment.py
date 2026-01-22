# =========================
# environment.py
# =========================
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from constants import (
    N, WALL_N, WALL_E, WALL_S, WALL_W,
    DIR_TO_VEC, LEFT_TURN, RIGHT_TURN, BACK_TURN,
    Action, Percept
)

def _wall_bit_for_dir(d: str) -> int:
    return {"N": WALL_N, "E": WALL_E, "S": WALL_S, "W": WALL_W}[d]


@dataclass
class RobotState:
    r: int
    c: int
    heading: str


class MazeEnv:
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
        for c in range(N):
            if not self._has_wall(0, c, "N"):
                raise ValueError("Top boundary missing NORTH wall")
            if not self._has_wall(N - 1, c, "S"):
                raise ValueError("Bottom boundary missing SOUTH wall")
        for r in range(N):
            if not self._has_wall(r, 0, "W"):
                raise ValueError("Left boundary missing WEST wall")
            if not self._has_wall(r, N - 1, "E"):
                raise ValueError("Right boundary missing EAST wall")

    def get_percept(self) -> Percept:
        r, c, h = self.robot.r, self.robot.c, self.robot.heading
        front = self._has_wall(r, c, h)
        left = self._has_wall(r, c, LEFT_TURN[h])
        right = self._has_wall(r, c, RIGHT_TURN[h])
        return Percept(front, left, right, (r, c), h)

    def step(self, action: Action) -> None:
        if action is None:
            return

        self.steps += 1
        r, c, h = self.robot.r, self.robot.c, self.robot.heading

        # Macro-actions: LEFT/RIGHT include a turn then a forward move
        if action == Action.LEFT:
            self.robot.heading = LEFT_TURN[h]
            h = self.robot.heading
            action = Action.FORWARD

        elif action == Action.RIGHT:
            self.robot.heading = RIGHT_TURN[h]
            h = self.robot.heading
            action = Action.FORWARD

        elif action == Action.U_TURN:
            self.robot.heading = BACK_TURN[h]
            return

        if action == Action.FORWARD:
            if self._has_wall(r, c, h):
                return  # blocked
            dr, dc = DIR_TO_VEC[h]
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                self.robot.r, self.robot.c = nr, nc
            return

        raise ValueError(f"Unknown action: {action}")
