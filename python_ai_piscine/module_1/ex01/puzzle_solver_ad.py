from __future__ import annotations
from collections import deque
from copy import deepcopy
import numpy as np
import sys
import random
import traceback


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


class Solver:
    steps = 0
    goal_state = (0, 1, 2,
                  3, 4, 5,
                  6, 7, 8)
    
    def solve_puzzle(self, puzzle: Puzzle) -> None:
        print("Initial state of the puzzle:\n")
        print(puzzle)

        if not puzzle.is_solvable:
            print("Puzzle is unsolvable!")
            return

        start_state = tuple(deepcopy(puzzle.grid_array))
        stack = [(start_state, (start_state,))]
        best_depth = float("inf")
        best_solution = None
        visited_depths = {}

        # cur_depth counts amount of moves made
        while stack:
            self.steps += 1
            cur_state, visited = stack.pop()
            cur_depth = len(visited) - 1

            prev_depth = visited_depths.get(cur_state)
            
            if prev_depth is not None and prev_depth <= cur_depth:
                continue
            visited_depths[cur_state] = cur_depth

            if cur_depth >= best_depth:
                continue

            if cur_state == self.goal_state:
                best_depth = cur_depth
                best_solution = visited
                print(f"Solving in {best_depth} moves")
                continue

            next_states = self.node_expansion(list(cur_state))
            next_states.sort(key=manhattan_distance, reverse=True)

            for next_state in next_states:
                if next_state not in visited:
                    next_depth = cur_depth + 1
                    lower_bound = next_depth + manhattan_distance(next_state)
                    if lower_bound < best_depth:
                        stack.append((next_state, visited + (next_state,)))

        if best_solution:
            print(f"\nShortest path found: {best_depth} moves")
            for step, state in enumerate(best_solution):
                print(f"\nStep {step}:")
                print(format_grid(state))
            print(f"Total Boards explored: {self.steps}")

    def node_expansion(self, cur_state: list) -> tuple:
        start_index = cur_state.index(0)
        start_pos = np.array([start_index // 3, start_index % 3])
        result = []

        up = start_pos[0] - 1
        down = start_pos[0] + 1
        left = start_pos[1] - 1
        right = start_pos[1] + 1

        if up >= 0 and up <= 2:
            target_index = up * 3 + start_pos[1]
            next_state = tuple(swap(target_index, cur_state.copy()))
            result.append(next_state)
        if down >= 0 and down <= 2:
            target_index = down * 3 + start_pos[1]
            next_state = tuple(swap(target_index, cur_state.copy()))
            result.append(next_state)
        if left >= 0 and left <= 2:
            target_index = start_pos[0] * 3 + left
            next_state = tuple(swap(target_index, cur_state.copy()))
            result.append(next_state)
        if right >= 0 and right <= 2:
            target_index = start_pos[0] * 3 + right
            next_state = tuple(swap(target_index, cur_state.copy()))
            result.append(next_state)
        return result  


def manhattan_distance(state: tuple) -> int:
    distance = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        goal_index = value
        row, column = divmod(index, 3)
        goal_row, goal_column = divmod(goal_index, 3)
        distance += abs(row - goal_row) + abs(column - goal_column)
    return distance


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
