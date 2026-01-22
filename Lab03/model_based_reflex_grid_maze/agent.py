# =========================
# agent.py
# =========================

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

from constants import N, Action, Percept, LEFT_TURN, RIGHT_TURN, BACK_TURN, DIR_TO_VEC


class ModelBasedReflexMazeAgent:
    """
    Model-based reflex agent for a known maze:
    - Maintains internal state: visited counts per cell.
    - Uses condition-action rules (no global planning).
    - Action set: TURN_LEFT / TURN_RIGHT / U_TURN / FORWARD.
    """

    def __init__(self, goal: Tuple[int, int]):
        self.goal = goal
        self.visit_count = [[0 for _ in range(N)] for _ in range(N)]
        self.prev_pos: Optional[Tuple[int, int]] = None  # helps avoid oscillation

    def reset(self) -> None:
        self.visit_count = [[0 for _ in range(N)] for _ in range(N)]
        self.prev_pos = None

 
    def act(self, percept: Percept) -> Action:
        (r, c) = percept.position

        # Update internal state
        self.visit_count[r][c] += 1

        # If at goal, do nothing meaningful; choose a safe action
        # (If you prefer, add Action.STOP to enum and return STOP)
        if (r, c) == self.goal:
            return Action.U_TURN  # or Action.FORWARD (will be blocked by wall sometimes)

        candidates = self._candidate_moves(percept)

        # If no candidates, safe fallback
        if not candidates:
            return Action.U_TURN

        # Rule 1: reach goal if possible
        for rel_action, (nr, nc) in candidates:
            if (nr, nc) == self.goal:
                return self._to_action(rel_action)

        # Rule 2/3: choose least-visited, tie-break LEFT > FORWARD > RIGHT
        preferred_order = {"LEFT": 0, "FORWARD": 1, "RIGHT": 2}
        scored = []
        for rel_action, (nr, nc) in candidates:
            v = self.visit_count[nr][nc]
            scored.append((v, preferred_order[rel_action], rel_action, (nr, nc)))
        scored.sort(key=lambda x: (x[0], x[1]))

        best_rel = scored[0][2]
        best_next = scored[0][3]

        # Anti-oscillation (optional)
        if self.prev_pos is not None and best_next == self.prev_pos and len(scored) > 1:
            best_rel = scored[1][2]
            best_next = scored[1][3]

        self.prev_pos = (r, c)
        return self._to_action(best_rel)  # <-- final guaranteed return


    def _candidate_moves(self, percept: Percept) -> List[Tuple[str, Tuple[int, int]]]:
        """
        Returns list of (relative_move, next_cell) where relative_move in {"LEFT","FORWARD","RIGHT"}.
        Uses percept walls to check legality.
        """
        r, c = percept.position
        h = percept.heading

        results: List[Tuple[str, Tuple[int, int]]] = []

        # LEFT move means: TURN_LEFT then FORWARD (we model as choosing TURN_LEFT now)
        if not percept.left_wall:
            nh = LEFT_TURN[h]
            dr, dc = DIR_TO_VEC[nh]
            results.append(("LEFT", (r + dr, c + dc)))

        # FORWARD
        if not percept.front_wall:
            dr, dc = DIR_TO_VEC[h]
            results.append(("FORWARD", (r + dr, c + dc)))

        # RIGHT
        if not percept.right_wall:
            nh = RIGHT_TURN[h]
            dr, dc = DIR_TO_VEC[nh]
            results.append(("RIGHT", (r + dr, c + dc)))

        # Filter out-of-bounds defensively (bounds should be protected by walls)
        filtered = []
        for rel, (nr, nc) in results:
            if 0 <= nr < N and 0 <= nc < N:
                filtered.append((rel, (nr, nc)))
        return filtered

    def _to_action(self, rel: str) -> Action:
        # Convert a relative move choice to the immediate action
        if rel == "LEFT":
            return Action.TURN_LEFT
        if rel == "RIGHT":
            return Action.TURN_RIGHT
