# =========================
# agent_goal_based.py
# =========================
from __future__ import annotations
from typing import List, Optional, Tuple

from constants import Action, Percept, LEFT_TURN, RIGHT_TURN, BACK_TURN
from search import bfs_path

def _turn_needed(current_heading: str, target_heading: str) -> Optional[Action]:
    """
    Returns LEFT/RIGHT/U_TURN if needed to face target_heading; None if already facing it.
    Uses macro-actions LEFT/RIGHT that include a forward move, so in this agent:
    - If turn needed, we return LEFT/RIGHT (it will move forward same step).
    - If already facing, return FORWARD.
    """
    if current_heading == target_heading:
        return None
    if LEFT_TURN[current_heading] == target_heading:
        return Action.LEFT
    if RIGHT_TURN[current_heading] == target_heading:
        return Action.RIGHT
    if BACK_TURN[current_heading] == target_heading:
        return Action.U_TURN
    return None

def _dir_from_to(a: Tuple[int, int], b: Tuple[int, int]) -> str:
    ar, ac = a
    br, bc = b
    if br == ar - 1 and bc == ac:
        return "N"
    if br == ar + 1 and bc == ac:
        return "S"
    if br == ar and bc == ac + 1:
        return "E"
    if br == ar and bc == ac - 1:
        return "W"
    raise ValueError(f"Cells not adjacent: {a}->{b}")


class GoalBasedMazeAgent:
    """
    Goal-based agent:
    - Has explicit goal.
    - Computes a shortest path plan using BFS on the known maze.
    - Executes the plan step-by-step (replans if needed).
    """

    def __init__(self, walls: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]):
        self.walls = walls
        self.start = start
        self.goal = goal
        self.plan_cells: Optional[List[Tuple[int, int]]] = None
        self.plan_index: int = 0

    def reset(self) -> None:
        self.plan_cells = None
        self.plan_index = 0

    def _ensure_plan(self, current_pos: Tuple[int, int]) -> None:
        self.plan_cells = bfs_path(self.walls, current_pos, self.goal)
        self.plan_index = 0

    def act(self, percept: Percept) -> Action:
        cur = percept.position
        h = percept.heading

        if cur == self.goal:
            return Action.U_TURN  # terminal anyway

        if self.plan_cells is None:
            self._ensure_plan(cur)

        if self.plan_cells is None:
            # no path exists
            return Action.U_TURN

        # If current position doesn't match plan (e.g., due to unexpected), replan
        if self.plan_index >= len(self.plan_cells) or self.plan_cells[self.plan_index] != cur:
            self._ensure_plan(cur)
            if self.plan_cells is None:
                return Action.U_TURN

        # We are at plan_cells[plan_index]. Next should be plan_cells[plan_index+1]
        if self.plan_index == len(self.plan_cells) - 1:
            return Action.U_TURN  # already at goal (should have been caught)

        nxt = self.plan_cells[self.plan_index + 1]
        target_heading = _dir_from_to(cur, nxt)

        turn_action = _turn_needed(h, target_heading)

        if turn_action == Action.U_TURN:
            # U_TURN does not move; next step we will face correct direction and go forward
            return Action.U_TURN

        if turn_action is None:
            # Facing correct direction: go forward to nxt
            self.plan_index += 1
            return Action.FORWARD

        # LEFT/RIGHT are macro-actions that also move forward -> we will reach nxt in same step
        self.plan_index += 1
        return turn_action
