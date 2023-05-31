import pygame
import sys
import time
# Define constants for the width and height of each grid cell
CELL_SIZE = 50
# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
BLUE = (0,0,255)
# Initialize Pygame
pygame.init()
delay = 0.03

# Define the maze layout, 0 is a path
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
# Create a window
window = pygame.display.set_mode((len(maze[0])*CELL_SIZE, len(maze)*CELL_SIZE))

# Directions
directions = ['up', 'right', 'down', 'left']

class Robot:
    def __init__(self, initial_pos=None, initial_dir=None):
        self.pos = initial_pos
        self.dir = initial_dir

    def move_forward(self):
        ahead = self.get_front_cell()
        if ahead == 1:
            return
        elif ahead == 2:
            pygame.quit()
            sys.exit()
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
        if instruction == [0,0,0,0,0,0,1,1]:
            self.move_forward()
        elif instruction == [0,0,0,0,0,0,0,1]:
            self.turn_left()
        elif instruction == [0,0,0,0,0,0,1,0]:
            self.turn_right()
        draw(self)
        time.sleep(delay)


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
        front = self.get_front_cell()
        #convert to byte
        if front == 0:
            return [0,0,0,0,0,0,0,0]
        elif front == 1:
            return [0,0,0,0,0,0,0,1]
        elif front == 2:
            return [0,0,0,0,0,0,1,0]



def draw(robot):
    # Draw the maze
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



