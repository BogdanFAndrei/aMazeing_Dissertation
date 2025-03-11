
import pygame, sys
from button import Button
from lib.amazeing import AMazeing

pygame.init()

SCREEN = pygame.display.set_mode((1280, 900))
pygame.display.set_caption("Solving Procedural Mazes using Algorithm")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def first_maze(): # this will be the first maze using Astar algorithm as solving method

    maze = AMazeing(search_algorithm="Solver")

    def main():
            maze.update()
           
    
    if __name__ == "__main__":
        while True:
            main()
    
def second_maze(): # this is the second maze which uses bfs as solving method
    maze = AMazeing(search_algorithm="BFS")

    def main():
            maze.update()
           
    
    if __name__ == "__main__":
        while True:
            main()
    
       
       
def third_maze(): # this is the third maze which eventually will use DFS as solving method 
    maze = AMazeing(search_algorithm="DFS")

    def main():
            maze.update()
           
    
    if __name__ == "__main__":
        while True:
            main()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        FIRSTMAZE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="A-STAR", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        SECONDMAZE_BUTTON = Button(image=pygame.image.load("assets/BFS BTN.png"), pos=(640, 400), 
                            text_input="BREADTH-FIRST-SEARCH", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        THIRDMAZE_BUTTON = Button(image=pygame.image.load("assets/BFS BTN.png"), pos=(640, 550), 
                            text_input="DEPTH-FIRST-SEARCH", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 700), 
                            text_input="Quit", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [FIRSTMAZE_BUTTON, SECONDMAZE_BUTTON, THIRDMAZE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FIRSTMAZE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    first_maze()
                if SECONDMAZE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    second_maze()
                if THIRDMAZE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    third_maze()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()



