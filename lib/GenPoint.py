import random
from Main import ADJACENTS, ADJWALLS, OPWALLS

##
#  GenPoint:  Generate Points
#
##
class GenPoint:
    #to allow for multiple generation points I pull this info into a seperate class
    def __init__(self,gencell,border):
        self.gencell     = gencell
        self.gen_id       = None
        self.genbound    = 0b0000
        self.current_cell = []
        self.visited   = {}
        self.border    = border
        self.stack = [[],[],[],[]]
        self.myneighbors = self.get_neighbors(self.gencell[0])
        self.get_gen_bounds()
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def get_neighbors(self,cell):
        #returns the neighbors as well as the direction that would take you there
        neighbors = []
        for i,adj in enumerate(ADJACENTS):
            check = (cell[0]+adj[0],cell[1]+adj[1])
            if check not in self.border:
                neighbors.append((check,ADJWALLS[i]))
        return neighbors

    def get_gen_bounds(self):
        for neighb in self.myneighbors:
            self.genbound |= OPWALLS[neighb[1]]
        self.gencell = (self.gencell[0],self.genbound)