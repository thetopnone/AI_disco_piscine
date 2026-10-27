import numpy as np
import math
import sys
import random
from copy import deepcopy


class Puzzle:
    solved_grid = [0, 1, 2,
                   3, 4, 5,
                   6, 7, 8]

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
        res = "Initial state of the puzzle:\n"
        return res + f"{self.grid[0]}\n{self.grid[1]}\n{self.grid[2]}\n"
    
    
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
    grid_states = []
    grid = []
    solved_grid = []

    def swap(self, target: int, grid: list) -> list:
        grid[grid.index(0)] = grid[target]
        grid[target] = 0
        return grid

    def heuristic(self, grid: list) -> int:
        solved_grid = [0, 1, 2,
                       3, 4, 5,
                       6, 7, 8]
        manhattan_dist = 0

        for row in range(3):
            for column in range(3):
                y = solved_grid.index(grid[row * 3 + column])
                sol_row = y // 3
                sol_column = y % 3
                manhattan_dist += (abs(row - sol_row) + abs(column - sol_column))
        return manhattan_dist

    def get_possible_neighbours(self,  grid: list) -> list:
        start_index = grid.index(0)
        start_pos = np.array([start_index // 3, start_index % 3])
        #print(start_pos)

        up = start_pos[0] - 1
        down = start_pos[0] + 1
        left = start_pos[1] - 1
        right = start_pos[1] + 1

        neighbours = []
        if up >= 0 and up <= 2:
            target_index = up * 3 + start_pos[1]
            neighbour = self.swap(target_index, grid.copy())
            neighbours.append(neighbour)
        if down >= 0 and down <= 2:
            target_index = down * 3 + start_pos[1]
            neighbour = self.swap(target_index, grid.copy())
            neighbours.append(neighbour)
        if left >= 0 and left <= 2:
            target_index = start_pos[0] * 3 + left
            neighbour = self.swap(target_index, grid.copy())
            neighbours.append(neighbour)
        if right >= 0 and right <= 2:
            target_index = start_pos[0] * 3 + right
            neighbour = self.swap(target_index, grid.copy())
            neighbours.append(neighbour)
        return neighbours

    def solve_puzzle(self, puzzle: Puzzle) -> None:
        print(puzzle)
        print(puzzle.is_solvable)
        print("Solving the puzzle...")

        if puzzle.is_solvable is False:
            print("Puzzle is unsolvable!")
            return

        alpha = 0.999
        for restarts in range(10):
            cur_grid = deepcopy(puzzle.grid_array)
            h_cur = self.heuristic(cur_grid)
            temp = 10.0

            while h_cur > 0 and temp > 0.001:
                neighbours = self.get_possible_neighbours(cur_grid)
                selected_neighbour = random.choice(neighbours)
                dh = h_cur - self.heuristic(selected_neighbour)

                if dh >= 0:
                    self.steps += 1
                    self.grid_states.append(selected_neighbour)
                    cur_grid = selected_neighbour
                    h_cur = self.heuristic(selected_neighbour)
                else:
                    probability = math.exp(dh / temp)
                    if random.random() < probability:
                        self.steps += 1
                        self.grid_states.append(selected_neighbour)
                        cur_grid = selected_neighbour
                        h_cur = self.heuristic(selected_neighbour)                        
                temp *= alpha
            if h_cur == 0:
                return


        #Finds which neighbours are better that the current pos
        #best_neighbour = self.neighbour_selection(puzzle.grid_array, good_neighbours)
        #print (best_neighbour)
            #self.grid = neighbour_selection(good_neighbours) #Selects the neighbour that has the highest probability to be good
            #self.grid_states.append(self.grid)
    


        
        
        


def main() -> int:
    puzzle1 = Puzzle(False)
    puzzle2 = Puzzle(True)

    solver = Solver()

    
    #print(puzzle1)
    #print(puzzle1.is_solvable)
    #solver.heuristic(puzzle1.grid_array)
    #print(puzzle2  )
    #print(puzzle2.is_solvable)
    #solver.heuristic(puzzle2.grid_array)
    solver.solve_puzzle(puzzle1)
    for state in solver.grid_states:
        print(state)

    return 0

if __name__ == "__main__":
    sys.exit(main())
