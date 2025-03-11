import random
import sys
import pygame
from lib.CellDraw import _CellDraw
from Main import COLORSCHOSEN, LISTSIZE, OPWALLS, SCREEN, SIZEMAZE, mazebar, montserrat, montserratsmall, pressed, checkbox
from lib.GenPoint import GenPoint
from lib.algorithms.DFS import DFS
from lib.algorithms.Astar import Solver
from lib.algorithms.BFS import BFS


class AMazeing(_CellDraw):
    #Primary maze generator
    def __init__(self, search_algorithm):
        self.search_algorithm = search_algorithm
       
        self.screen  = SCREEN
        self.animate = True
        self.loops   = False
        self.reset   = False
        self.difcol  = False
       
        #This is the percent chance of revisiting a cell and creating a loop if 'loops' is on.
        #Putting this much above 1% gets silly really quickly. Possibly even lower would be better.
        self.loopchance = 1
        
        self.clock   = pygame.time.Clock()
      
        self.sizeind = 4
        self.wallind = 2
        self.init()
        
    def init(self):
        #used for resetting without altering user preferences
        self.state       = "START"
        self.calc_size()
        self.drawn       = False
        self.solvetime   = False
        
        self.genpoints = [] #a list of GenPoint classes
        self.gen_ids    = None
        self.starting_cell = None
        self.goal_cell  = None
        
        self.border    = set()
        self.visited   = set()
        self.neighbors = {}
        self.dirdict   = {}

        #generates the border with regards to the cell size
        #if generators are allowed in the border it must be two cells thick (at least)
        for i in range(self.screen.get_width()//self.cell_size[0]):
            self.border |= set(((i, 0),))
            self.border |= set(((i, -1),))##
            self.border |= set(((i,SIZEMAZE[1]//self.cell_size[1]-1),))
            self.border |= set(((i,SIZEMAZE[1]//self.cell_size[1]),))##
        for j in range(SIZEMAZE[1]//self.cell_size[1]):
            self.border |= set((( 0,j),))
            self.border |= set((( -1,j),))##
            self.border |= set(((self.screen.get_width()//self.cell_size[0]-1,j),))
            self.border |= set(((self.screen.get_width()//self.cell_size[0],j),))##

        self.time_start = 0.0
        self.timeend   = 0.0

        #used for solving
        self.searching = None
        self.answer  = None
        self.MySolver  = None

        #button's pressed
        self.startpress = False
        self.resetpress = False

        self.gentime = ""
        self.slvtime = ""
        self.length  = ""
        print("BORDER:  ", self.border)   
  

    def calc_size(self):
        self.core_size   = LISTSIZE[self.sizeind]
        self.wall_size   = LISTSIZE[self.wallind]
        self.cell_size   = tuple(self.core_size[i]+self.wall_size[i] for i in range(2))
        self.buffer_settings = ((SIZEMAZE[0] % self.cell_size[0]-self.wall_size[0])//2,
                       (SIZEMAZE[1] % self.cell_size[1]-self.wall_size[1])//2)
        

    def draw(self):
        if self.state != "GENERATE":
            self.screen.fill((0,0,0),((0,0),SIZEMAZE))
        self.screen.fill(COLORSCHOSEN["border_line"],((0,0),(SIZEMAZE[0],self.cell_size[1]+self.buffer_settings[1])))
        self.screen.fill(COLORSCHOSEN["border_line"],((0,0),(self.cell_size[0]+self.buffer_settings[0],SIZEMAZE[1])))
        self.screen.fill(COLORSCHOSEN["border_line"],((0,(SIZEMAZE[1]//self.cell_size[1]-1)*self.cell_size[1]+self.buffer_settings[1]+self.wall_size[1]),
                                           (SIZEMAZE[0],self.cell_size[1]+self.buffer_settings[1]+10)))
        
        self.screen.fill(COLORSCHOSEN["border_line"],(((SIZEMAZE[0]//self.cell_size[0]-1)*self.cell_size[0]+self.buffer_settings[0]+self.wall_size[0],0),                                           
                                           (self.cell_size[0]+self.buffer_settings[0]+10,SIZEMAZE[1])))
        self.maze_bar()
        if not self.animate and self.state in ("SOLVED","DONE") or self.reset:
            if self.difcol:
                for gen in self.genpoints:
                    for cell in gen.visited:
                        self.draw_cell((cell,gen.visited[cell]),gen.color)
            else:
                for cell in self.dirdict:
                    self.draw_cell((cell,self.dirdict[cell]),COLORSCHOSEN["halls"])
            self.reset = False
        if self.searching:
            for cell in self.searching:
                if cell not in [self.starting_cell,self.goal_cell]:
                    self.draw_cell((cell,self.dirdict[cell]),COLORSCHOSEN["search_path"])
            self.draw_core((self.starting_cell,self.dirdict[self.starting_cell]),COLORSCHOSEN["start_color"])
            self.draw_walls((self.starting_cell,self.dirdict[self.starting_cell]),COLORSCHOSEN["search_path"])
        if self.answer:
            for cell in self.answer:
                if cell != self.goal_cell:
                    self.draw_core((cell,None),COLORSCHOSEN["solution_color"])
            for cell in self.MySolver.solwalls:
                    self.draw_walls((cell,self.MySolver.solwalls[cell]),COLORSCHOSEN["solution_color"])
            self.draw_core((self.goal_cell,self.dirdict[self.goal_cell]),COLORSCHOSEN["goal_color"])
            self.draw_core((self.starting_cell,self.dirdict[self.starting_cell]),COLORSCHOSEN["start_color"])
      


    def maze_bar(self):
        self.screen.blit(mazebar,(0,800))
        self.screen.blit(montserratsmall.render(str(self.core_size[0]).zfill(2),1,COLORSCHOSEN["halls"]),(763,SIZEMAZE[1]+42))
        self.screen.blit(montserratsmall.render(str(self.wall_size[0]).zfill(2),1,COLORSCHOSEN["halls"]),(671,SIZEMAZE[1]+42))
        if   self.state == "START":
            self.screen.blit(montserrat.render("Click on the dark screen to place generation Points",1,(0,0,0)),(270,SIZEMAZE[1]+6))
        elif self.state == "READY":
            self.screen.blit(montserrat.render("Click 'start' or press space to begin generation",1,(0,0,0)),(225,SIZEMAZE[1]+6))
        elif   self.state == "DONE":
            if not self.starting_cell:
                self.screen.blit(montserrat.render("Please place your start point.",1,(0,0,0)),(295,SIZEMAZE[1]+6))
            else:
                self.screen.blit(montserrat.render("Please place your goal point.",1,(0,0,0)),(295,SIZEMAZE[1]+6))
        elif   self.state == "SOLVE":
            self.screen.blit(montserrat.render("Press 'space' or click start to solve your maze.",1,(0,0,0)),(225,SIZEMAZE[1]+6)) 
        if self.gentime:
            self.screen.blit(montserratsmall.render("generation time (ms)",1,(0,0,0)),(5,SIZEMAZE[1]+6))
            self.screen.blit(montserratsmall.render(": "+self.gentime,1,(0,0,0)),(130,SIZEMAZE[1]+6))
        if self.slvtime:
            self.screen.blit(montserratsmall.render("Solve time (ms)",1,(0,0,0)),(5,SIZEMAZE[1]+18))
            self.screen.blit(montserratsmall.render(": "+self.slvtime,1,(0,0,0)),(130,SIZEMAZE[1]+18))
            self.screen.blit(montserratsmall.render("Path length (cells)",1,(0,0,0)),(5,SIZEMAZE[1]+30))
            self.screen.blit(montserratsmall.render(": "+self.length,1,(0,0,0)),(130,SIZEMAZE[1]+30))
        if not self.animate:
            self.screen.blit(checkbox,(114,SIZEMAZE[1]+62))
        if not self.loops:
            self.screen.blit(checkbox,(212,SIZEMAZE[1]+62))

                 
    def cell_targ(self):
        return ((self.target[0]-self.buffer_settings[0])//self.cell_size[0],(self.target[1]-self.buffer_settings[1])//self.cell_size[1])


    def event_loop(self):
        self.target = pygame.mouse.get_pos()
        for click in pygame.event.get():
            if click.type == pygame.MOUSEBUTTONDOWN:
                hit = pygame.mouse.get_pressed()
                if hit[0]:
                    self.target = pygame.mouse.get_pos()
                    if (0 < self.target[0] < self.screen.get_width()) and (0 < self.target[1] < SIZEMAZE[1]):
                        #place start/goal
                        if self.state == "START":
                            self.place_gen()
                        elif self.state == "DONE":
                            self.place_goal()
                    #reset button
                    elif 300 < self.target[0] < 400 and (SIZEMAZE[1]+40 < self.target[1] < SIZEMAZE[1]+90):
                        self.init()
                        self.resetpress = True
                    #start button
                    elif 425 < self.target[0] < 525 and (SIZEMAZE[1]+40 < self.target[1] < SIZEMAZE[1]+90):
                        self.start_it()
                    #toggle animation on/off
                    elif 31 < self.target[0] < 128 and (SIZEMAZE[1]+59 < self.target[1] < SIZEMAZE[1]+77):
                        self.tog_anim()
                    #toggle loops on/off
                    elif 146 < self.target[0] < 226 and (SIZEMAZE[1]+59 < self.target[1] < SIZEMAZE[1]+77):
                        self.tog_loop()

                    if self.state not in ["GENERATE","SOLVING"]:
                        #make cell size bigger/smaller
                        if   759 < self.target[0] < 779 and (SIZEMAZE[1]+18 < self.target[1] < SIZEMAZE[1]+38):
                            self.node_up()
                        elif 759 < self.target[0] < 779 and (SIZEMAZE[1]+61 < self.target[1] < SIZEMAZE[1]+81):
                            self.node_down()
                        #make walls thinner/thicker
                        elif 667 < self.target[0] < 687 and (SIZEMAZE[1]+18 < self.target[1] < SIZEMAZE[1]+38):
                            self.wall_up()
                        elif 667 < self.target[0] < 687 and (SIZEMAZE[1]+61 < self.target[1] < SIZEMAZE[1]+81):
                            self.wall_down()

            #hotkeys      
            if click.type == pygame.KEYDOWN:
                #start
                if click.key == pygame.K_SPACE:
                    self.start_it()
                #reset
                elif click.key == pygame.K_RETURN:
                    self.init()
                    self.resetpress = True
                #toggle animation
                elif click.key == pygame.K_d:
                    self.tog_anim()
                #toggle loops on/off
                elif click.key == pygame.K_l:
                    self.tog_loop()
                #resets maze to unsolved (essentially a refresh key)
                elif click.key == pygame.K_i:
                    if self.state != "GENERATE":
                        self.initial()
                #toggle generator specific colors on/off (refresh after pressing if not mid-generation)
                elif click.key == pygame.K_c:
                    self.difcol = (True if not self.difcol else False)
                    if self.state != "START":
                        self.reset = True
                        self.draw()
                        pygame.display.update()
                    
                #change cell size
                if self.state not in ["GENERATE","SOLVING"]:
                    if   click.key in [pygame.K_KP_PLUS,pygame.K_PLUS,pygame.K_EQUALS]:
                        self.node_up()
                    elif click.key in [pygame.K_KP_MINUS,pygame.K_MINUS] :
                        self.node_down()
                #quit
                if click.key == pygame.K_ESCAPE:
                    self.state = "QUIT"

            #reset start/reset buttons to unpushed
            if click.type in [pygame.MOUSEBUTTONUP,pygame.KEYUP]:
                if   self.startpress:
                    self.startpress = False
                    self.screen.blit(mazebar,(425,SIZEMAZE[1]+40),(425,40,100,50))
                    pygame.display.update()
                elif self.resetpress:
                    self.resetpress = False
                    self.screen.blit(mazebar,(300,SIZEMAZE[1]+40),(300,40,100,50))
                    pygame.display.update()
                    
            if click.type == pygame.QUIT: self.state = "QUIT"

        #make start/reset buttons pushed
        if self.startpress:
            self.screen.blit(pressed,(425,SIZEMAZE[1]+40))
            pygame.display.update()
        elif self.resetpress:
            self.screen.blit(pressed,(300,SIZEMAZE[1]+40))
            pygame.display.update()



    def initial(self):
        #resets maze to an unsolved state without deleting current maze
        history = self.dirdict
        gens    = self.genpoints
        self.init()
        self.dirdict   = history
        self.genpoints = gens
        self.state     = "DONE"
        self.solvetime = True
        self.drawn     = False
        self.reset     = True
        

    #raise and lower cell size
    def node_up(self):
        if self.sizeind < len(LISTSIZE)-1:
            self.sizeind += 1
            self.init()

    def node_down(self):
        if self.sizeind > 0:
            self.sizeind -= 1
            self.init()

    def wall_up(self):
        if self.wallind < len(LISTSIZE)-1:
            self.wallind += 1
            self.init()

    def wall_down(self):
        if self.wallind > 0:
            self.wallind -= 1
            self.init()

###########################AStar Variables###################################################
    def create_solver_Astar(self):
        self.MySolver = Solver(self.starting_cell,self.goal_cell,self.dirdict,self.animate,self.screen)
        self.MySolver.time_start = pygame.time.get_ticks()
        self.MySolver.get_openset()
        self.MySolver.cell_size = self.cell_size
        self.MySolver.wall_size = self.wall_size
        self.MySolver.core_size = self.core_size
        self.MySolver.buffer_settings    = self.buffer_settings
        self.state = "SOLVING"


###########################BFS Variables###################################################
    def create_solver_BFS(self):
       self.MySolver = BFS(self.starting_cell, self.goal_cell, self.dirdict, self.animate, self.screen)
       self.MySolver.time_start = pygame.time.get_ticks()
       self.MySolver.get_openset()
       self.MySolver.cell_size = self.cell_size
       self.MySolver.wall_size = self.wall_size
       self.MySolver.core_size = self.core_size
       self.MySolver.buffer_settings = self.buffer_settings
       self.state = "SOLVING"


###########################DFS Variables###################################################
    def create_solver_DFS(self):
        self.MySolver = DFS(self.starting_cell, self.goal_cell, self.dirdict, self.animate, self.screen)
        self.MySolver.time_start = pygame.time.get_ticks()
        self.MySolver.cell_size = self.cell_size
        self.MySolver.wall_size = self.wall_size
        self.MySolver.core_size = self.core_size
        self.MySolver.buffer_settings = self.buffer_settings
        self.state = "SOLVING"

    #toggle animation on/off
    def tog_anim(self):
        self.animate = (True if not self.animate else False)
        if self.MySolver:
            self.MySolver.animate = self.animate
        if self.animate:
            #regards toggling animation on/off during generation or solving
            if self.state == "GENERATE":
                for gen in self.genpoints:
                    for cell in gen.visited:
                        if not self.difcol:
                            self.draw_cell((cell,gen.visited[cell]),COLORSCHOSEN["halls"])
                        else:
                            self.draw_cell((cell,gen.visited[cell]),gen.color)
            elif self.state == "SOLVING":
                if self.searching:
                    for cell in self.searching:
                        if cell not in [self.starting_cell,self.goal_cell]:
                            self.draw_cell((cell,self.dirdict[cell]),COLORSCHOSEN["search_path"])
                    self.draw_cell((self.starting_cell,self.dirdict[self.starting_cell]),COLORSCHOSEN["start_color"])
                if self.answer:
                    for cell in self.answer:
                        if cell != self.goal_cell:
                            self.draw_core((cell,None),COLORSCHOSEN["solution_color"])
                    for cell in self.MySolver.solwalls:
                            self.draw_walls((cell,self.MySolver.solwalls[cell]),COLORSCHOSEN["solution_color"])
                    self.draw_core((self.goal_cell,self.dirdict[self.goal_cell]),COLORSCHOSEN["goal_color"])
                    self.draw_core((self.starting_cell,self.dirdict[self.starting_cell]),COLORSCHOSEN["start_color"])   
            self.screen.blit(mazebar,(114,SIZEMAZE[1]+61),(114,61,13,13))
        else:
            self.screen.blit(checkbox,(114,SIZEMAZE[1]+61))
        pygame.display.update()
    
    
    #toggle loops on/off
    def tog_loop(self):
        self.loops = (False if self.loops else True)
        if self.loops:
            self.screen.blit(mazebar,(212,SIZEMAZE[1]+61),(212,61,13,13))
        else:
            self.screen.blit(checkbox,(212,SIZEMAZE[1]+61))
        pygame.display.update()
       

    #start button functionality
    def start_it(self):
        if self.genpoints and not self.solvetime and self.state != "GENERATE":
            self.state = "GENERATE"
            self.time_start = pygame.time.get_ticks()
            if self.animate:
                for gen in self.genpoints:
                    for check in self.neighbors[gen.gencell[0]]:
                        if not self.difcol:
                            self.draw_cell(check,COLORSCHOSEN["halls"])
                        else:
                            self.draw_cell(check,gen.color)
                    self.screen.fill((0,0,0),((gen.gencell[0][0]*self.cell_size[0]+self.buffer_settings[0],
                                               gen.gencell[0][1]*self.cell_size[1]+self.buffer_settings[1]),self.cell_size))
                    if not self.difcol:
                        self.draw_cell(gen.gencell,COLORSCHOSEN["halls"])
                    else:
                        self.draw_cell(gen.gencell,gen.color)
        elif self.state == "SOLVE":
          
            ##################!######################################################################################################  
            ##################!######## Here is the solving called on the maze ######################################################
            ##################V######################################################################################################
           
            if self.search_algorithm == "Solver":
                            
                self.create_solver_Astar()  # Create A* solver object
                 
                self.startpress = True
                
                self.maze_bar()
                
                pygame.display.update()  
                #runs until now

            elif self.search_algorithm == "BFS":
            
                self.create_solver_BFS()  # Create BFS solver object
                self.startpress = True
               
                self.maze_bar()
               
                pygame.display.update()  
                #runs until now
            elif self.search_algorithm == "DFS":
            
                self.create_solver_DFS()  # Create DFS solver object
                self.startpress = True
               
                self.maze_bar()
               
                pygame.display.update()  
                #runs until now

        
    #place generator points
    def place_gen(self):
        gencell = (self.cell_targ(),0b0000)
        new_gen = GenPoint(gencell,self.border)

        if self.check_overlap(new_gen):
            if not self.gen_ids:
                new_gen.gen_id = 1
                self.gen_ids  = 1
            else:
                self.gen_ids  <<= 1
                new_gen.gen_id = (self.gen_ids)
            self.genpoints.append(new_gen)
            self.neighbors[gencell[0]] = new_gen.myneighbors     
            for j,cell in enumerate(new_gen.myneighbors):
                new_gen.current_cell.append(cell)
                new_gen.stack[j].append(cell[0])
                self.dirdict[cell[0]]   = cell[1]
                new_gen.visited[cell[0]] = cell[1]
            while [] in new_gen.stack:
                new_gen.stack.remove([])
            new_gen.visited[new_gen.gencell[0]] = new_gen.gencell[1]
            self.dirdict[new_gen.gencell[0]] = new_gen.gencell[1]
            for vis in new_gen.visited:
                self.visited |= set((vis,))
            self.visited |= set((new_gen.gencell[0],))
            self.screen.fill(COLORSCHOSEN["start_color"],((gencell[0][0]*self.cell_size[0]+self.buffer_settings[0],
                                                 gencell[0][1]*self.cell_size[1]+self.buffer_settings[1]),self.cell_size))
            self.maze_bar()
            pygame.display.update()



    def check_overlap(self,gen):
        #This deals with generators being placed close together.
        for other_gen in self.genpoints:
            if   gen.gencell[0] == other_gen.gencell[0]:
                return 0
            else:
                checklist = gen.myneighbors[:]
                for vis,way in checklist:  
                    if vis in other_gen.visited:
                        gen.myneighbors.remove((vis,way))
                        gen.get_gen_bounds()
                    if vis == other_gen.gencell[0]:
                        if gen.gencell[0] in other_gen.visited:
                            other_gen.visited.pop(gen.gencell[0])
                        for cell in other_gen.current_cell:
                            if cell[0] == gen.gencell[0]:
                                other_gen.current_cell.remove(cell)
                                other_gen.myneighbors.remove(cell)
                                other_gen.get_gen_bounds()
                                other_gen.visited[other_gen.gencell[0]] = other_gen.gencell[1]
                                self.dirdict[other_gen.gencell[0]] = other_gen.gencell[1]
                        for stack in other_gen.stack:
                            for cell in stack:
                                if cell == gen.gencell[0]:
                                    other_gen.stack.remove(stack)
                                    break
        return 1
                 


    #placing start/goal cells
    def place_goal(self):
        if not self.starting_cell:
            self.starting_cell = self.cell_targ()
            self.draw_core((self.starting_cell,None),COLORSCHOSEN["start_color"])
        else:
            self.goal_cell = self.cell_targ()
            self.border.discard(self.goal_cell)
            self.visited |= set((self.goal_cell,))
            self.state = "SOLVE"
            self.draw_core((self.goal_cell,None),COLORSCHOSEN["goal_color"])
        self.maze_bar()
        pygame.display.update()



    def generation(self):
        def gen_anim(gen,check):
            if self.animate:
                if not self.difcol:
                    self.draw_cell(check,COLORSCHOSEN["halls"])
                else:
                    self.draw_cell(check,gen.color)


        def merge_gens(gen,other_gen,check):
            #Logic for allowing a cell to 'revisit' another cell 
            #thereby connecting generators or creating a loop.
            updatecell      = (gen.current_cell[i][0],gen.current_cell[i][1] | OPWALLS[check[1]])
            otherupdatecell = (check[0],other_gen.visited[check[0]] | check[1]) 
            gen.visited[updatecell[0]]  = updatecell[1]
            self.dirdict[updatecell[0]] = updatecell[1]                                           
            other_gen.visited[otherupdatecell[0]] = otherupdatecell[1]
            self.dirdict[otherupdatecell[0]]     = otherupdatecell[1]
            for k,cell in enumerate(other_gen.current_cell):
                if cell and cell[0] == check[0]:
                    other_gen.current_cell[k] = otherupdatecell
            gen.current_cell[i] = updatecell

            if self.animate:
                if not self.difcol:
                    self.draw_walls(updatecell,COLORSCHOSEN["halls"])
                    self.draw_walls((check[0],other_gen.visited[check[0]]),COLORSCHOSEN["halls"])
                else:
                    self.draw_walls(updatecell,gen.color)
                    self.draw_walls((check[0],other_gen.visited[check[0]]),other_gen.color)
                pygame.display.update()

        #Definately a little messy on determining when to stop but works. (I'm sure there is an easier, simpler way)
        go = False
        for gen in self.genpoints:
            if go: break
            for stack in gen.stack:
                go = (True if stack else False)
                if go: break
        for gen in self.genpoints:
            if self.state == "DONE":
                break
            for stack in gen.stack:
                if go:
                    for i in range(len(gen.stack)):
                        if gen.current_cell[i]:
                            if gen.current_cell[i][0] not in self.neighbors:
                                self.neighbors[gen.current_cell[i][0]] = gen.get_neighbors(gen.current_cell[i][0])                                
                            if self.neighbors[gen.current_cell[i][0]]:
                                check = random.choice(self.neighbors[gen.current_cell[i][0]])
                                self.neighbors[gen.current_cell[i][0]].remove(check)
                                if check[0] not in self.border:
                                    for other_gen in self.genpoints:
                                        if check[0] not in self.visited:
                                            updatecell = (gen.current_cell[i][0],gen.current_cell[i][1] | OPWALLS[check[1]])
                                            gen.visited[updatecell[0]] = updatecell[1]
                                            self.dirdict[updatecell[0]] = updatecell[1]
                                            if self.animate:
                                                if not self.difcol:
                                                    self.draw_walls(updatecell,COLORSCHOSEN["halls"])
                                                else:
                                                    self.draw_walls(updatecell,gen.color)
                                                pygame.display.update()
                                            gen.stack[i].append(check[0])
                                            self.dirdict[check[0]] = check[1]
                                            gen.current_cell[i] = check
                                            gen.visited[check[0]] = check[1]
                                            self.visited |= set ((check[0],))
                                            gen_anim(gen,check)
                                            break
                                        elif not (gen.gen_id & other_gen.gen_id) and check[0] in other_gen.visited:
                                            merge_gens(gen,other_gen,check)
                                            #The below logic assures that generators only connect once,
                                            #thereby retaining a perfect maze (unless of course 'loops' is on).
                                            new_id = gen.gen_id | other_gen.gen_id
                                            thisold = gen.gen_id ; otherold = other_gen.gen_id
                                            for id in self.genpoints:
                                                if id.gen_id in [thisold,otherold]:
                                                    id.gen_id = new_id
                                            break
                                        elif self.loops:
                                            #Reconnect to a visited cell at the chance set in 'self.loopchance'.
                                            chance = random.randint(1,100)
                                            if chance <= self.loopchance and check[0] in other_gen.visited:
                                                merge_gens(gen,other_gen,check)
                                                break
                                    else:
                                        self.dirdict[gen.current_cell[i][0]] = gen.current_cell[i][1]
                            else:
                                if gen.stack[i]:
                                    popped = gen.stack[i].pop()
                                    gen.current_cell[i] = (popped,self.dirdict[popped])
                                else:
                                    gen.current_cell[i] = None
                else:
                    self.timeend = pygame.time.get_ticks()
                    self.gentime = str(self.timeend-self.time_start)
                    self.solvetime = True
                    self.state = "DONE"
                    self.maze_bar()
                    pygame.display.update()
                    if not self.animate:
                        self.drawn = False
                    break
     
    def update(self):
        if self.state not in  ["GENERATE","SOLVING"]:
            if not self.drawn:
                self.screen.fill(COLORSCHOSEN["halls"])
                self.draw()
                pygame.display.update()
                self.drawn = True
            self.event_loop()
        elif self.state == "GENERATE":
            if self.animate:
                pygame.display.update()
            self.generation()
            self.event_loop()
            pygame.event.pump()
        elif self.state == "SOLVING":
            if self.animate:
                pygame.display.update()
            if self.MySolver.solved:
                self.answer = self.MySolver.evaluation()
                self.slvtime = str(self.MySolver.timeend-self.MySolver.time_start)
                self.length = str(len(self.answer))
                self.state = "SOLVED"
                self.maze_bar()
                pygame.display.update()
                if not self.animate:
                    self.drawn = False
            else:
                result = self.MySolver.evaluation()
                if result:
                    self.searching = result
                else:
                    self.state = "SOLVED"
                    if not self.animate:
                        self.drawn = False
            self.event_loop()
            pygame.event.pump()
                    
        if self.state == "QUIT":
            pygame.quit();sys.exit()