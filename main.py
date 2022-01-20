import pygame, numpy, random


SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

GRIDSIZE = 20
GRID_WIDTH = 0
GRID_HEIGHT = 0

LIGHT, DARK = (93, 216, 228), (84, 194, 205)

UP = (0, -GRIDSIZE)
DOWN = (0, GRIDSIZE)
LEFT = (-GRIDSIZE, GRIDSIZE)
RIGHT = (GRIDSIZE, GRIDSIZE)
STAY = None

OCCUPIED, FREE = 0, 1


def get_matrix_from_file(path):
    # get file data
    # set width and height
    # get limits indexes
    lines = []
    global GRID_HEIGHT, GRID_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH

    with open(path) as file:
        lines = file.readlines()

    for line in range(len(lines) - 1):
        lines[line] = lines[line][:-1]

    GRID_WIDTH = len(lines[0])
    GRID_HEIGHT = len(lines) + 1
    SCREEN_WIDTH = GRID_WIDTH * GRIDSIZE
    SCREEN_HEIGHT = GRID_HEIGHT * GRIDSIZE
    
    limits_indexes = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '1':
                limits_indexes.append( (j, i) )

    return limits_indexes
    


class Field():
    '''
        This class is simply array GRID_WIDTH x GRID_HEIGHT
        Contains info if fields are FREE or OCCUPIED
        OCCUPIED means it contains limit particle or sand
        Initialy it is filled as FREE
    '''
    def __init__(self) -> None:
        self.matrix = numpy.empty( (GRID_WIDTH, GRID_HEIGHT) )
        self.matrix.fill(int(FREE))
    

    def set_occupied(self, index):
        self.matrix[ int(index[0]) ][ int(index[1]) ] = OCCUPIED


    def set_free(self, index):
        self.matrix[ int(index[0]) ][ int(index[1]) ] = FREE
    

    def not_occupied(self, index):
        if self.matrix[index[0], index[1]] == FREE:
            return True
        else:
            return False
    

    def is_inside(self, index):
        return 0 <= index[0] < GRID_WIDTH and 0 <= index[1] < GRID_HEIGHT
    

    def element_equals_to(self, x, y, element):
        if self.is_inside( (x, y) ):
            return self.matrix[int(x), int(y)] == element



class Sand():
    '''
        PARAM:
            self.position:
                An array contains tuple (pixel, pixel)
                At every change the position element is added to the array for setting the current position
    '''
    def __init__(self) -> None:
        self.position = [( ((SCREEN_WIDTH / 2), 0) )]
        self.color = (255, 255, 0)
    
    def draw(self, surface):
        r = pygame.Rect( (self.position[0][0], self.position[0][1]), (GRIDSIZE, GRIDSIZE) )
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, LIGHT, r, 1)


    def randomize_position(self):
        self.position[0] = ( random.randint(0, GRID_WIDTH-1) * GRIDSIZE, 0 * GRIDSIZE )
    
    def get_position(self):
        return self.position
    
    def get_index(self):
        return ( self.position[0][0] / GRIDSIZE, self.position[0][1] / GRIDSIZE )
    

    def check_below(self, field):
        index = self.get_index()

        # Is at the bottom
        if index[1] == GRID_HEIGHT - 1:
            return STAY

        # Check if the elements below are occupied
        if field.element_equals_to(index[0], index[1] + 1, FREE):
            # Directly below
            return DOWN
        elif field.element_equals_to(index[0] - 1, index[1] + 1, FREE):
            # On the left
            return LEFT
        elif field.element_equals_to(index[0] + 1, index[1] + 1, FREE):
            # On the right
            return RIGHT
        else:
            # Nowhere to go, nothing to do!
            return STAY
        

    def update(self, field):
        direction = self.check_below(field)
        if direction != STAY:
            field.set_free(self.get_index())
            new = (direction[0] + self.position[0][0], direction[1] + self.position[0][1])
            self.position.insert( 0, new )
            self.position.pop()
            field.set_occupied(self.get_index())


class Limit():
    def __init__(self) -> None:
        self.index = (12, 5)
        self.color = (153, 153, 153)
    

    def set_limit(self, field):
        field.set_occupied(self.index)
    

    def set_index(self, index):
        self.index = index
    

    def randomize_index(self):
        self.index = ( random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1) )
    

    def draw(self, surface):
        r = pygame.Rect( (self.index[0] * GRIDSIZE, self.index[1] * GRIDSIZE), (GRIDSIZE, GRIDSIZE) )
        pygame.draw.rect(surface, self.color, r)




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

    limits_indexes = get_matrix_from_file('test_skosy.txt')

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    game_board = Field()
    sandpile = []
    limits = []

    for i in range(len(limits_indexes)):
        limits.append(Limit())
        limits[i].set_index(limits_indexes[i])
        limits[i].set_limit(game_board)

    counter = 1
    ticker = 20

    run = True
    while run:
        clock.tick(ticker)

        if counter % 2:
            sand = Sand()
            sand.randomize_position()
            sandpile.append(sand)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ticker = 3
            elif event.type == pygame.MOUSEBUTTONUP:
                ticker = 20
        
        drawGrid(surface)

        for sand in sandpile:
            sand.draw(surface)
            sand.update(game_board)
        
        for limit in limits:
            limit.draw(surface)

        counter += 1
        screen.blit(surface, (0, 0))
        pygame.display.update()

    pygame.quit()




if __name__ == '__main__':
    main()