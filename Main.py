import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

SIZEMAZE   = (1280,800)
SIZESCREEN = (1280, 900)
SCREEN = pygame.display.set_mode(SIZESCREEN)

#graphics and fonts
mazebar    = pygame.image.load("assets/mazebar.png").convert()
checkbox   = pygame.image.load("assets/checkbox.png").convert()
pressed    = pygame.image.load("assets/pressed.png").convert_alpha()
montserratsmall = pygame.font.Font ("assets/Montserrat-Light.ttf",13)
montserrat = pygame.font.Font ("assets/Montserrat-Light.ttf",20)

#constant globals
COLORSCHOSEN  = {"start_color": (255, 155, 0),"goal_color":(0, 100, 255),"halls":(255, 255, 255),
             "search_path":(137, 207, 240),"solution_color": (0, 0, 139), "border_line": (139, 0, 139)}
LISTSIZE  = ((1,1),(2,2),(5,5),(10,10),(25,25),(50,50))
ADJACENTS = ((0,-1),(1,0),(0,1),(-1,0))
ADJWALLS  = (0b0010,0b0001,0b1000,0b0100)
OPWALLS   = {0b1000:0b0010,0b0100:0b0001,0b0010:0b1000,0b0001:0b0100}
CHECKADJ  = {(0,-1):0b1000,(1, 0):0b0100,(0, 1):0b0010,(-1,0):0b0001}
