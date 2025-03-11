import pygame
from lib.CellDraw import _CellDraw
from Main import ADJACENTS, CHECKADJ, COLORSCHOSEN, OPWALLS

class Solver(_CellDraw):
    def __init__(self,start,goal,visited,animate,screen):
        
        print("Initializing Astar Solver")

        print("THis is Astar")
        self.dirdict   = visited
        self.screen    = screen
        self.animate   = animate
        self.cell_size = (20,20)
        self.wall_size = (10,10)
        self.core_size = (10,10)
        self.solwalls  = {}
        self.buffer_settings    = (0,0)
        
        self.starting_cell   = start
        self.goal_cell    = goal
        self.current_cell = self.starting_cell
        self.nextcell    = None

        self.altmethod  = None
        self.solved     = False
        self.answer   = []

        self.time_start = 0.0
        self.timeend   = 0.0

        self.hx = {} #optimal estimate to goal
        self.gx = {} #cost from start to current position
        self.fx = {} #distance-plus-cost heuristic function

        self.close_setting = set()
        self.openset   = set()
        self.gx[self.starting_cell] = 0
        self.hx[self.starting_cell] = self.get_distance(self.starting_cell,self.goal_cell)

        self.close_setting |= set((self.starting_cell,))
        self.came_from  = {}

        self.state    = None
        self.pathdone = False
        self.path_time = False

    def get_distance(self,start,goal):
        #optimum path distance for orthoganal movement 'Rook'
        distance = abs(goal[0]-start[0])+abs(goal[1]-start[1])
        return distance

    def get_neighbors(self):
        openset = set()
        for (i,j) in ADJACENTS:
            check = (self.current_cell[0]+i,self.current_cell[1]+j)
            if (CHECKADJ[(i,j)] & self.dirdict[self.current_cell]) and check not in self.close_setting:
                openset |= set((check,))
        return openset
                
    def get_openset(self):
        self.openset = self.get_neighbors()
        print("Openset:", self.openset)

    def get_path(self,cell):
        #Most of this is for aesthetic reasons.  I didn't like walls not directly on the path being filled.
        if cell in self.came_from:
            self.answer.append(cell)
            self.current_cell = self.came_from[cell]
            direction = (self.current_cell[0]-self.answer[-1][0],self.current_cell[1]-self.answer[-1][1])
            if self.animate:
                if self.current_cell not in (self.starting_cell,self.goal_cell):
                    self.draw_core((self.current_cell,None),COLORSCHOSEN["solution_color"])
                    if direction in [(0,1),(-1,0)]:
                        self.draw_walls((self.current_cell,OPWALLS[CHECKADJ[direction]]),COLORSCHOSEN["solution_color"])
                    else:
                        self.draw_walls((cell,CHECKADJ[direction]),COLORSCHOSEN["solution_color"])
            if direction in [(0,1),(-1,0)]:
                self.solwalls[self.current_cell] = self.solwalls.setdefault(self.current_cell,0) | OPWALLS[CHECKADJ[direction]]
            else:
                self.solwalls[cell] = self.solwalls.setdefault(cell,0) | CHECKADJ[direction]
        else:
            direction = (self.current_cell[0]-self.answer[-1][0],self.current_cell[1]-self.answer[-1][1])
            if self.animate:
                if direction in [(0,1),(-1,0)]:
                    self.draw_walls((cell,OPWALLS[CHECKADJ[direction]]),COLORSCHOSEN["solution_color"])
                else:
                    self.draw_walls((self.answer[-1],CHECKADJ[direction]),COLORSCHOSEN["solution_color"])
            if direction in [(0,1),(-1,0)]:
                self.solwalls[cell] = self.solwalls.setdefault(cell,0) | OPWALLS[CHECKADJ[direction]]
            else:
                print("DIRECTION:", direction)
                self.solwalls[self.answer[-1]] = self.solwalls.setdefault(self.answer[-1],0) | CHECKADJ[direction]
            self.pathdone = True

    def evaluation(self):
         print("Evaluating in Astar")
         if self.openset and not self.path_time:
             print("Openset:", self.openset)
             if self.nextcell:
                 print("Using nextcell:", self.nextcell)
                 self.current_cell = self.nextcell
             if not self.altmethod or not self.nextcell:
                 for cell in self.openset:
                     if cell not in self.came_from:
                         self.gx[cell] = 1
                         self.hx[cell] = self.get_distance(cell, self.goal_cell)
                         self.fx[cell] = self.gx[cell] + self.hx[cell]
                         self.came_from[cell] = self.starting_cell
                     if self.current_cell not in self.openset:
                         self.current_cell = cell
                     elif self.fx[cell] < self.fx[self.current_cell]:
                         self.current_cell = cell
        
             if self.current_cell == self.goal_cell:
                 print("Reached goal")
                 self.path_time = True
        
             self.openset.discard(self.current_cell)
             self.close_setting |= set((self.current_cell,))
             if self.animate:
                 if self.current_cell not in (self.starting_cell, self.goal_cell):
                     self.draw_cell((self.current_cell, self.dirdict[self.current_cell]), COLORSCHOSEN["search_path"])
                     self.draw_walls((self.starting_cell, self.dirdict[self.starting_cell]), COLORSCHOSEN["search_path"])



                     
        
             neighbors = self.get_neighbors()
             print("Neighbors:", neighbors)
             self.nextcell = None
             for cell in neighbors:
                 tent_g = self.gx[self.current_cell] + 1
                 if cell not in self.openset:
                     self.openset |= set((cell,))
                     tent_better = True
                 elif cell in self.gx and tent_g < self.gx[cell]:
                     tent_better = True
                 else:
                     tent_better = False
        
                 if tent_better:
                     self.came_from[cell] = self.current_cell
                     self.gx[cell] = tent_g
                     self.hx[cell] = self.get_distance(cell, self.goal_cell)
                     self.fx[cell] = self.gx[cell] + self.hx[cell]
                     if not self.nextcell:
                         self.nextcell = cell
                     elif self.fx[cell] < self.fx[self.nextcell]:
                         self.nextcell = cell
             return self.close_setting
         elif self.path_time and not self.pathdone:
             print("Getting path")
             self.get_path(self.current_cell)
             return self.close_setting
         elif self.pathdone:
             self.timeend = pygame.time.get_ticks()
             if not self.solved:
                 self.solved = True
                 print("Done")
                 self.state = "DONE"
                 return self.close_setting
             else:
                 return self.answer
         else:
             # reached if no answer is found or possible.
             # Beware that searching for a answer when no answer is possible is very time-consuming.
             self.timeend = pygame.time.get_ticks()
             self.state