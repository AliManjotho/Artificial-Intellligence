# =========================
# search.py
# =========================
from __future__ import annotations
from collections import deque
from typing import Dict, List, Optional, Tuple

from constants import N, WALL_N, WALL_E, WALL_S, WALL_W

def _has_wall(walls: List[List[int]], r: int, c: int, direction: str) -> bool:
    bit = {"N": WALL_N, "E": WALL_E, "S": WALL_S, "W": WALL_W}[direction]
    return (walls[r][c] & bit) != 0

def neighbors(walls: List[List[int]], r: int, c: int) -> List[Tuple[int, int, str]]:
    """
    Returns list of (nr, nc, dir) where dir is the absolute direction you move.
    """
    nbrs: List[Tuple[int, int, str]] = []
    # N
    if not _has_wall(walls, r, c, "N") and r - 1 >= 0:
        nbrs.append((r - 1, c, "N"))
    # E
    if not _has_wall(walls, r, c, "E") and c + 1 < N:
        nbrs.append((r, c + 1, "E"))
    # S
    if not _has_wall(walls, r, c, "S") and r + 1 < N:
        nbrs.append((r + 1, c, "S"))
    # W
    if not _has_wall(walls, r, c, "W") and c - 1 >= 0:
        nbrs.append((r, c - 1, "W"))
    return nbrs

def bfs_path(walls: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    BFS shortest path in an unweighted grid maze.
    Returns list of cells from start->goal inclusive, or None if no path.
    """
    q = deque([start])
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    while q:
        cur = q.popleft()
        if cur == goal:
            # reconstruct path
            path = []
            node: Optional[Tuple[int, int]] = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path

        r, c = cur
        for nr, nc, _ in neighbors(walls, r, c):
            nxt = (nr, nc)
            if nxt not in parent:
                parent[nxt] = cur
                q.append(nxt)

    return None
