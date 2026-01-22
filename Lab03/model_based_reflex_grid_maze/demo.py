# =========================
# demo_main.py
# =========================

from __future__ import annotations
from typing import List
from constants import N, WALL_N, WALL_E, WALL_S, WALL_W, Action
from environment import MazeEnv
from agent import ModelBasedReflexMazeAgent

def make_sample_maze_8x8() -> List[List[int]]:
    """
    A small, valid 8x8 maze (outer walls closed). Internal walls are simple and not necessarily a 'perfect maze'.
    You can replace this with your own known maze map.

    NOTE: Each cell has boundary walls; internal walls are added symmetrically by hand.
    """
    # Start with all outer walls + no internal walls
    walls = [[0 for _ in range(N)] for _ in range(N)]

    # Add outer boundary walls
    for c in range(N):
        walls[0][c] |= WALL_N
        walls[N-1][c] |= WALL_S
    for r in range(N):
        walls[r][0] |= WALL_W
        walls[r][N-1] |= WALL_E

    # Helper to add a wall between two adjacent cells (bidirectional)
    def add_wall(r: int, c: int, d: str):
        nonlocal walls
        if d == "N":
            walls[r][c] |= WALL_N
            walls[r-1][c] |= WALL_S
        elif d == "S":
            walls[r][c] |= WALL_S
            walls[r+1][c] |= WALL_N
        elif d == "E":
            walls[r][c] |= WALL_E
            walls[r][c+1] |= WALL_W
        elif d == "W":
            walls[r][c] |= WALL_W
            walls[r][c-1] |= WALL_E
        else:
            raise ValueError(d)

    # Add a few internal walls (keep them symmetric via add_wall)
    add_wall(0, 1, "S")
    add_wall(1, 1, "E")
    add_wall(1, 2, "S")
    add_wall(2, 2, "E")
    add_wall(2, 3, "E")
    add_wall(3, 3, "S")
    add_wall(4, 3, "E")
    add_wall(4, 4, "S")
    add_wall(5, 4, "E")
    add_wall(5, 5, "S")
    add_wall(6, 5, "E")
    add_wall(6, 6, "S")

    return walls

def run_episode(max_steps: int = 500) -> None:
    walls = make_sample_maze_8x8()
    env = MazeEnv(walls=walls, start=(0, 0), goal=(7, 7), start_heading="E")
    agent = ModelBasedReflexMazeAgent(goal=(7, 7))

    step = 0
    while not env.is_terminal() and step < max_steps:
        percept = env.get_percept()
        action = agent.act(percept)
        env.step(action)
        step += 1

    print(f"Terminal: {env.is_terminal()} | Steps: {env.steps} | Final: {(env.robot.r, env.robot.c)}")

if __name__ == "__main__":
    run_episode()
