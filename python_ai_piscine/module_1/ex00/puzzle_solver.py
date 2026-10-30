from __future__ import annotations
from copy import deepcopy
import numpy as np
import sys
import random


def format_grid(grid: list) -> str:
    values = []
    if grid and isinstance(grid[0], list):
        for row in grid:
            for value in row:
                values.append(value)
    else:
        values = grid
    rows = []
    for row in range(0, 9, 3):
        rows.append(f"[{values[row]}, {values[row + 1]}, {values[row + 2]}]")
    return "\n".join(rows)


class State:
    def __init__(self, _grid: list[int], _prev_path_cost: int, _parent: State):
        self.parents: list[State] = []
        if _parent is not None:
            self.parents = _parent.parents.copy()
            self.parents.append(_parent)
        self.grid = deepcopy(_grid)
        self.grid_key = tuple(self.grid)
        self.path_cost = _prev_path_cost + 1
        self.estimated_cost = heuristic(_grid)
        self.total_cost = self.path_cost + self.estimated_cost

    def __str__(self) -> str:
        return format_grid(self.grid)

    def node_expansion(self) -> list:
        start_index = self.grid.index(0)
        start_pos = divmod(start_index, 3)
        neighbours = []

        moves = [(1,0),
                (-1,0),
                (0, 1),
                (0, -1)]

        for move in moves:
            next_pos = (start_pos[0] + move[0], start_pos[1] + move[1])
            if next_pos[0] >= 0 and next_pos[0] < 3 and next_pos[1] >= 0 and next_pos[1] < 3:
                next_index = next_pos[0] * 3 + next_pos[1]
                neighbor_grid = swap(next_index, self.grid.copy())
                neighbor = State(neighbor_grid, self.path_cost, self)
                neighbours.append(neighbor)
        return neighbours
        
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
    steps = -1

    def __init__(self):
        self.frontier_set: list[State] = []
        self.frontier_map: dict[touple[int,...]: State] = {}
        self.explored_set = set()

    def solve_puzzle(self, puzzle: Puzzle) -> None:
        print("Initial state of the puzzle:\n")
        print(puzzle)
        print("Solving the puzzle...")
        if puzzle.is_solvable is False:
            print("Puzzle is unssolvable!")
            return
        initial_state = State(puzzle.grid_array, -1, None)
        goal_state = puzzle.solved_grid
        self.frontier_set = [initial_state]
        self.frontier_map = {initial_state.grid_key : initial_state}
        self.explored_set = set()

        while self.frontier_set:
            self.steps += 1
            current_state = self.select_next_state()

            if current_state.grid_key == goal_state:
                moves = len(current_state.parents)
                print("Solution found!")
                print(f"Moves: {moves}" )
                current_state.parents.append(current_state)
                for i in range(len(current_state.parents)):
                    print(f"\nStep {i}:")
                    print(current_state.parents[i])
                print(f"Boards Explored: {self.steps}")
                return

            self.explored_set.add(current_state.grid_key)
            neighbours = current_state.node_expansion()
            self.evaluate_neighbours(neighbours)

    def evaluate_neighbours(self, neighbours: list[State]) -> None:
        frontier = self.frontier_set
        frontier_map = self.frontier_map
        for state in neighbours:
            if state.grid_key in self.explored_set:
                continue
            elif state.grid_key not in frontier_map:
                frontier.append(state)
                frontier_map[state.grid_key] = state
            elif state.grid_key in frontier_map:
                temp = frontier_map[state.grid_key]
                if state.total_cost < temp.total_cost:
                    frontier.remove(temp)
                    frontier_map[state.grid_key] = state
                    frontier.append(state)

         
    def select_next_state(self) -> State:
        frontier = self.frontier_set
        frontier_map  = self.frontier_map
        if len(frontier) == 1:
            res = deepcopy(frontier[0])
            frontier_map.pop(res.grid_key)
            frontier.pop(0)
            return res

        lowest_total_cost = float('inf')
        lowest_estimated_cost = float('inf')
        selected_state = None
        for state in frontier:
            cur_total_cost = state.total_cost
            cur_estimated_cost = state.estimated_cost
            if cur_total_cost < lowest_total_cost:
                lowest_total_cost = cur_total_cost
                lowest_estimated_cost = cur_estimated_cost
                selected_state = state
            elif cur_total_cost == lowest_total_cost and cur_estimated_cost < lowest_estimated_cost:
                lowest_total_cost = cur_total_cost
                lowest_estimated_cost = cur_estimated_cost
                selected_state = state
        res = deepcopy(selected_state)
        frontier_map.pop(res.grid_key)
        frontier.remove(selected_state)
        return res

                    
def heuristic(grid: list) -> int:
    solved_grid = (0, 1, 2,
                   3, 4, 5,
                   6, 7, 8)
    manhattan_dist = 0

    for row in range(3):
        for column in range(3):
            y = solved_grid.index(grid[row * 3 + column])
            sol_row = y // 3
            sol_column = y % 3
            manhattan_dist += (abs(row - sol_row) + abs(column - sol_column))
    return manhattan_dist


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
