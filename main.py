from logging.handlers import WatchedFileHandler
from tkinter import RIGHT
import pygame


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

LIGHT = (93, 216, 228)
DARK = (84, 194, 205)

UP = (0, -GRIDSIZE)
DOWN = (0, GRIDSIZE)
LEFT = (-GRIDSIZE, 0)
RIGHT = (GRIDSIZE, 0)


class Void(object):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.position = (x, y)
        self.occupied = False
    

    def is_occupied(self):
        return self.occupied
    

    def draw(self, surface, colour):
        r = pygame.Rect( (self.position[0]*GRIDSIZE, self.position[1]*GRIDSIZE), (GRIDSIZE, GRIDSIZE) )
        pygame.draw.rect(surface, colour, r)



class Sand(object):
    def __init__(self) -> None:
        super().__init__()
        self.position = [( ((SCREEN_WIDTH / 2), 0) )]
        self.color = (255, 255, 0)
    
    def draw(self, surface):
        r = pygame.Rect( (self.position[0][0], self.position[0][1]), (GRIDSIZE, GRIDSIZE) )
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, LIGHT, r, 1)


    def randomize_position():
        pass
    
    def get_position(self):
        return self.position
    

    def check_below(self):
        pass
        

    def update(self):
        if self.position[0][1] == SCREEN_HEIGHT - GRIDSIZE:
            return
        new = (DOWN[0] + self.position[0][0], DOWN[1] + self.position[0][1])
        self.position.insert( 0, new )
        self.position.pop()



def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect( (x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE) )
                pygame.draw.rect(surface, LIGHT, r)
            else:
                r = pygame.Rect( (x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE) )
                pygame.draw.rect(surface, DARK, r)



def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    sand = Sand()

    run = True
    while run:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        drawGrid(surface)
        sand.draw(surface)

        sand.update()

        screen.blit(surface, (0, 0))
        pygame.display.update()

    pygame.quit()




if __name__ == '__main__':
    main()