from __future__ import annotations
from copy import deepcopy
import numpy as np
import math
import sys
import random


def format_grid(grid: list) -> str:
    if grid and isinstance(grid[0], list):
        values = [value for row in grid for value in row]
    else:
        values = grid
    rows = []
    for row in range(0, 9, 3):
        rows.append(
            f"[{values[row]}, {values[row + 1]}, {values[row + 2]}]"
        )
    return "\n".join(rows)
        
class Puzzle:
    solved_grid = (0, 1, 2,
                   3, 4, 5,
                   6, 7, 8)

    def __init__(self, default_seed: bool):
        self.grid = []
        self.grid_array = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.is_default_seed = False
        self.is_solvable = True

        if default_seed is True:
            
            self.grid = [[7, 5, 0],
                         [6, 4, 1],
                         [8, 3, 2]]
            self.grid_array = [7, 5, 0, 6, 4, 1, 8, 3, 2]
            self.is_default_seed = True
        else:
            self.generate_grid()

    def __str__(self) -> str:
        return format_grid(self.grid)
    
    
    def generate_grid(self) -> None:
        if self.is_default_seed is True:
            return
        numbers = list(range(9))
        random.shuffle(numbers)
        self.grid_array = numbers.copy()
        self.parity_check(numbers.copy())
        for i in range(0, 9, 3):
            self.grid.append(numbers[i:i + 3])

    def parity_check(self, numbers: list) -> None:
        inversions = 0

        numbers.remove(0)
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] > numbers[j]:
                    inversions += 1
        if inversions % 2 == 1:
            self.is_solvable = False

class State:
    def __init__(self, _grid: list[int], _parent: State):
        self.parents: list[State] = []
        if _parent is not None:
            self.parents = _parent.parents.copy()
            self.parents.append(_parent)
        self.grid = deepcopy(_grid)

    def __str__(self) -> str:
        return format_grid(self.grid)

    def node_expansion(self) -> list:
        
        
        neighbours = []
        if up >= 0 and up <= 2:
            target_index = up * 3 + start_pos[1]
            neighbor_grid = swap(target_index, self.grid.copy())
            neighbours.append(neighbor)
        if down >= 0 and down <= 2:
            target_index = down * 3 + start_pos[1]
            neighbor_grid = swap(target_index, self.grid.copy())
            neighbours.append(neighbor)
        if left >= 0 and left <= 2:
            target_index = start_pos[0] * 3 + left
            neighbor_grid = swap(target_index, self.grid.copy())
            neighbours.append(neighbor)
        if right >= 0 and right <= 2:
            target_index = start_pos[0] * 3 + right
            neighbor_grid = swap(target_index, self.grid.copy())
            neighbours.append(neighbor_grid)
        return neighbours

class Solver:
    steps = -1

    def __init__(self):
        self.frontier_set: list[State] = []
        self.explored_set = set()

    def solve_puzzle(self, puzzle: Puzzle) -> None:
        goal_state = puzzle.solved_grid
        cur_state = State(puzzle.grid_array, None)
        frontier = self.frontier_set
        explored = self.explored_set
        frontier.append(cur_state)

        while is frontier:
            explored.add(cur_state)
            frontier.remove(cur_state)
            neighbours = cur_state.node_expansion()
            start_index = self.grid.index(0)
            start_pos = np.array([start_index // 3, start_index % 3])
                    
            up = start_pos[0] - 1
            down = start_pos[0] + 1
            left = start_pos[1] - 1
            right = start_pos[1] + 1


                
        
            
        
def solve_puzzle(cur_grid: list[int], previous_steps: list[list[int]]) -> list:
    next_grid: list[int] = []

    

def swap(target: int, grid: list) -> list:
        grid[grid.index(0)] = grid[target]
        grid[target] = 0
        return grid


def main() -> int:
    try:
        if len(sys.argv) == 2:
            if sys.argv[1] != "default":
                raise Exception("Invalid Format! Try using: python3 "
                                "./ex00/puzzle_solver.py (default)")
            else:
                puzzle = Puzzle(True)
                solver = Solver()
                solver.solve_puzzle(puzzle)
                return
        elif len(sys.argv) != 1:
            raise Exception("Invalid Format! Try using: python3 "
                            "./ex00/puzzle_solver.py (default)")
    
        puzzle = Puzzle(False)
        solver = Solver()
        solver.solve_puzzle(puzzle)
        return 0
    except Exception as err:
        print(err.args[0], file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
