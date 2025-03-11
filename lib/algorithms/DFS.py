import pygame
from lib.CellDraw import _CellDraw
from Main import ADJACENTS, CHECKADJ, COLORSCHOSEN, OPWALLS

class DFS(_CellDraw):
    def __init__(self, start, goal, visited, animate, screen):
        super().__init__()  # Call superclass's __init__() method
        print("Initializing DFS Solver")
        self.dirdict = visited
        self.screen = screen
        self.animate = animate
        self.cell_size = (20, 20)
        self.wall_size = (10, 10)
        self.core_size = (10, 10)
        self.solwalls = {}
        self.buffer_settings = (0, 0)
 
        self.starting_cell = start
        self.goal_cell = goal
        self.current_cell = self.starting_cell
        self.solved = False
        self.answer = []
 
        self.close_setting = set()
        self.stack = []  # Initialize stack for DFS
 
        self.close_setting |= set((self.starting_cell,))
        self.came_from = {}
 
        self.state = None
        self.pathdone = False
        self.path_time = False
        print("Current cell:", self.current_cell)
        print("Direction dictionary:", self.dirdict)
 
    def get_distance(self, start, goal):
        # Optimum path distance for orthogonal movement 'Rook'
        distance = abs(goal[0] - start[0]) + abs(goal[1] - start[1])
        return distance
    
 
    def get_neighbors(self):
        neighbors = []
        if self.current_cell in self.dirdict:
            for (i, j) in ADJACENTS:
                check = (self.current_cell[0] + i, self.current_cell[1] + j)
                # Check if the neighboring cell is within reach and not in the closed set
                if (CHECKADJ[(i, j)] & self.dirdict[self.current_cell]) and check not in self.close_setting:
                    neighbors.append(check)
        return neighbors
 
    def evaluation(self):
        print("Evaluating in DFS")
 
        # Start: Push the starting node onto a stack. Mark the starting node as visited.
        if not self.path_time:
            if self.current_cell != self.goal_cell:
                print("Exploring neighbors:")

                for cell in self.get_neighbors():
                    if cell not in self.close_setting:
                        self.stack.append(cell)  # Push each adjacent node onto the stack
                        self.came_from[cell] = self.current_cell
                        self.close_setting.add(cell)  # Mark each adjacent node as visited to avoid revisiting
                        if self.animate:
                            if cell not in (self.starting_cell, self.goal_cell):
                                self.draw_cell((cell, self.dirdict[cell]), COLORSCHOSEN["search_path"])
                                self.draw_walls((self.current_cell, self.dirdict[self.current_cell]), COLORSCHOSEN["search_path"])
 
                if self.stack:
                    self.current_cell = self.stack.pop()  # Pop the top cell from the stack
                    print("New current cell:", self.current_cell)
                else:
                    # No more cells to explore, change state to SOLVED
                    self.state = "SOLVED"
        
                    return None
                return self.close_setting    

            else:
                print("Reached goal")
                self.state = "SOLVED"
                self.path_time = True
                self.get_path(self.current_cell)  # Get the path when goal is reached
                return self.answer
 
        elif self.pathdone:
            self.timeend = pygame.time.get_ticks()
            if not self.solved:
                self.solved = True
                print("Solved in", self.timeend - self.time_start, "ms")
                print("Path found")
                self.state = "DONE"
                return self.close_setting
            else:
                self.state = "DONE"
                return self.answer

    
      
 
    def get_path(self, cell):
        # A loop for drawing the path based on the came_from dictionary
        while cell in self.came_from:
            self.answer.append(cell)
            self.current_cell = self.came_from[cell]
            direction = (self.current_cell[0] - self.answer[-1][0], self.current_cell[1] - self.answer[-1][1])
            if self.animate:
                if self.current_cell not in (self.starting_cell, self.goal_cell):
                    self.draw_core((self.current_cell, None), COLORSCHOSEN["solution_color"])
                    if direction in [(0, 1), (-1, 0)]:
                        self.draw_walls((self.current_cell, OPWALLS[CHECKADJ[direction]]), COLORSCHOSEN["solution_color"])
                    else:
                        self.draw_walls((cell, CHECKADJ[direction]), COLORSCHOSEN["solution_color"])
            if direction in [(0, 1), (-1, 0)]:
                self.solwalls[self.current_cell] = self.solwalls.setdefault(self.current_cell, 0) | OPWALLS[CHECKADJ[direction]]
            else:
                self.solwalls[cell] = self.solwalls.setdefault(cell, 0) | CHECKADJ[direction]
            cell = self.current_cell
 
        # Draw remaining walls if any
        if self.animate:
            for i in range(1, len(self.answer)):
                current_cell = self.answer[i]
                previous_cell = self.answer[i - 1]
                direction = (current_cell[0] - previous_cell[0], current_cell[1] - previous_cell[1])
                if direction in [(0, 1), (-1, 0)]:
                    self.draw_walls((previous_cell, CHECKADJ[direction]), COLORSCHOSEN["solution_color"])
                elif direction in [(0, -1), (1, 0)]:
                    self.draw_walls((current_cell, OPWALLS[CHECKADJ[direction]]), COLORSCHOSEN["solution_color"])
                else:
                    self.draw_core((current_cell, None), COLORSCHOSEN["solution_color"])
 
        self.pathdone = True