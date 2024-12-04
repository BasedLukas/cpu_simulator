import time 

CELL_SIZE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
BLUE = (0,0,255)

delay = 0.05 # speed of the animation
directions = ['up', 'right', 'down', 'left']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 2],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


# Helper function to convert RGB tuples to CSS strings
def rgb_to_css(rgb_tuple):
    return f'rgb({rgb_tuple[0]}, {rgb_tuple[1]}, {rgb_tuple[2]})'


def draw_web(robot: "Robot"):
    """Draw the maze and robot on the canvas."""
    context = robot.context
    canvas = robot.canvas
    # Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height)
    
    # Draw the maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect_x = x * CELL_SIZE
            rect_y = y * CELL_SIZE
            if maze[y][x] == 1:  # Wall
                context.fillStyle = rgb_to_css(BLACK)
            elif maze[y][x] == 2:  # End
                context.fillStyle = rgb_to_css(BLUE)
            else:  # Path
                context.fillStyle = rgb_to_css(WHITE)
            context.fillRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)
            context.strokeStyle = rgb_to_css(BLACK)
            context.strokeRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

    # Highlight the square ahead of the robot
    if robot.dir == 'up' and robot.pos[1] > 0:
        rect_x = robot.pos[0] * CELL_SIZE
        rect_y = (robot.pos[1] - 1) * CELL_SIZE
    elif robot.dir == 'right' and robot.pos[0] < len(maze[0]) - 1:
        rect_x = (robot.pos[0] + 1) * CELL_SIZE
        rect_y = robot.pos[1] * CELL_SIZE
    elif robot.dir == 'down' and robot.pos[1] < len(maze) - 1:
        rect_x = robot.pos[0] * CELL_SIZE
        rect_y = (robot.pos[1] + 1) * CELL_SIZE
    elif robot.dir == 'left' and robot.pos[0] > 0:
        rect_x = (robot.pos[0] - 1) * CELL_SIZE
        rect_y = robot.pos[1] * CELL_SIZE
    else:
        rect_x = robot.pos[0] * CELL_SIZE
        rect_y = robot.pos[1] * CELL_SIZE
    context.fillStyle = rgb_to_css(GREEN)
    context.fillRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

    # Draw the robot
    rect_x = robot.pos[0] * CELL_SIZE
    rect_y = robot.pos[1] * CELL_SIZE
    context.fillStyle = rgb_to_css(RED)
    context.fillRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)


def draw_pygame(robot:"Robot" ,delay=0.01):
    """Pass in a robot object and draw the maze and robot"""
    pygame = robot.pygame
    window = robot.window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:  # wall
                pygame.draw.rect(window, BLACK, rect)
            elif maze[y][x] == 2:  # end
                pygame.draw.rect(window, BLUE, rect)
            else:  # path
                pygame.draw.rect(window, WHITE, rect)


    # Draw the square ahead of the robot
    if robot.dir == 'up' and robot.pos[1] > 0:
        rect = pygame.Rect(robot.pos[0]*CELL_SIZE, (robot.pos[1]-1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    elif robot.dir == 'right' and robot.pos[0] < len(maze[0]) - 1:
        rect = pygame.Rect((robot.pos[0]+1)*CELL_SIZE, robot.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    elif robot.dir == 'down' and robot.pos[1] < len(maze) - 1:
        rect = pygame.Rect(robot.pos[0]*CELL_SIZE, (robot.pos[1]+1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    elif robot.dir == 'left' and robot.pos[0] > 0:
        rect = pygame.Rect((robot.pos[0]-1)*CELL_SIZE, robot.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, GREEN, rect)
    # Draw the robot
    rect = pygame.Rect(robot.pos[0]*CELL_SIZE, robot.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, RED, rect)
    pygame.display.update()
    time.sleep(delay)


class Robot:
    def __init__(self, initial_pos=[1,1], initial_dir='up', pygame=None, window=None, context=None, canvas=None):
        """use pygame or js depending on platform"""
        self.pos = initial_pos.copy() # so we can restart
        self.dir = initial_dir
        self.pygame = pygame
        self.window = window
        self.context = context
        self.canvas = canvas
        msg = "Require either pygame+window or context + canvas"
        assert (pygame and window) or (context and canvas), msg


    def move_forward(self):
        ahead = self.get_front_cell()
        if ahead == 1:
            return
        elif ahead == 2:
            if self.pygame:
                self.pygame.quit()
                quit() 
            return
        if self.dir == 'up':
            self.pos[1] -= 1
        elif self.dir == 'right':
            self.pos[0] += 1
        elif self.dir == 'down':
            self.pos[1] += 1
        elif self.dir == 'left':
            self.pos[0] -= 1

    def turn_left(self):
        self.dir = directions[(directions.index(self.dir) - 1) % 4]

    def turn_right(self):
        self.dir = directions[(directions.index(self.dir) + 1) % 4]

    def move(self, instruction):
        """this function takes the cpu output and moves the robot accordingly"""
        if instruction == [0,0,0,0,0,0,1,1]:
            self.move_forward()
        elif instruction == [0,0,0,0,0,0,0,1]:
            self.turn_left()
        elif instruction == [0,0,0,0,0,0,1,0]:
            self.turn_right()
        if self.pygame:
            draw_pygame(self)
        else:
            draw_web(self)

    def get_front_cell(self):
        if self.dir == 'up':
            return maze[self.pos[1]-1][self.pos[0]]
        elif self.dir == 'right':
            return maze[self.pos[1]][self.pos[0]+1]
        elif self.dir == 'down':
            return maze[self.pos[1]+1][self.pos[0]]
        elif self.dir == 'left':
            return maze[self.pos[1]][self.pos[0]-1]
        
    def get_front_cell_bit(self):
        """This functions reads the front cell and passes it to the cpu input"""
        front = self.get_front_cell()
        #convert to byte
        if front == 0:
            return [0,0,0,0,0,0,0,0]
        elif front == 1:
            return [0,0,0,0,0,0,0,1]
        elif front == 2:
            if self.pygame:
                self.game.quit()
                quit() 
            return

