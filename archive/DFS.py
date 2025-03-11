
from Main import *


# this is a different type of implementation of DFS algorithm which will be needed for "Evaluation" function in DFS class 
def DFS(self):
    self.frontier = [self.start]
    self.explored = [self.start]
    self.dfsPath = {self.goal}

    while len(self.frontier)>0:
        currCell=self.frontier.pop()
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if self.maze[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in self.explored:
                    continue
                self.explored.append(childCell)
                self.frontier.append(childCell)
                self.dfsPath[childCell]=currCell
    fwdPath={}
 
    while cell!=self.start:
        fwdPath[self.dfsPath[cell]]=cell
        cell=self.dfsPath[cell]
    return fwdPath


if __name__ == '__main__':


    # Replace the following line with your maze generation code
    maze_generator = AMazeing()
    maze_generator.update()

    maze_object = maze_generator  # Assuming your maze object is created by the generator

   