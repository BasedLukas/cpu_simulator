import time
import micropip
import asyncio
import js
import pyodide
await micropip.install('dist/cpu-0.1.0-py3-none-any.whl')
from assembler.assembler import assemble_binary
from hardware.cpu import CPU

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


RESULT = "" # pyodide global
# Define colors as strings for canvas
WHITE = "white"
RED = "red"
GREEN = "green"
BLACK = "black"
BLUE = "blue"

# Get the canvas and its context
canvas = js.document.getElementById("mazeCanvas")
context = canvas.getContext('2d')

# Maze dimensions
CELL_SIZE = 20  # Adjust cell size as needed


# Adjust canvas size based on maze dimensions
canvas.width = len(maze[0]) * CELL_SIZE
canvas.height = len(maze) * CELL_SIZE

directions = ['up', 'right', 'down', 'left']
delay = 0.05  # Speed of the animation

class Robot:
    def __init__(self, initial_pos=[1, 1], initial_dir='up'):
        self.pos = initial_pos
        self.dir = initial_dir

    def move_forward(self):
        ahead = self.get_front_cell()
        if ahead == 1:
            return
        elif ahead == 2:
            js.alert("Robot reached the goal!")
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
        """Take the CPU output and move the robot accordingly."""
        if instruction == [0, 0, 0, 0, 0, 0, 1, 1]:
            self.move_forward()
        elif instruction == [0, 0, 0, 0, 0, 0, 0, 1]:
            self.turn_left()
        elif instruction == [0, 0, 0, 0, 0, 0, 1, 0]:
            self.turn_right()
        draw(self)

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
        """Reads the front cell and passes it to the CPU input."""
        front = self.get_front_cell()
        if front == 0:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        elif front == 1:
            return [0, 0, 0, 0, 0, 0, 0, 1]
        elif front == 2:
            js.alert("Robot reached the goal!")
            return

def draw(robot: Robot):
    """Draw the maze and robot on the canvas."""
    # Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height)
    
    # Draw the maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect_x = x * CELL_SIZE
            rect_y = y * CELL_SIZE
            if maze[y][x] == 1:  # Wall
                context.fillStyle = BLACK
            elif maze[y][x] == 2:  # End
                context.fillStyle = BLUE
            else:  # Path
                context.fillStyle = WHITE
            context.fillRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)
            context.strokeStyle = BLACK
            context.strokeRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

    # Highlight the square ahead of the robot
    if robot.dir == 'up' and robot.pos[1] > 0:
        rect_x = robot.pos[0] * CELL_SIZE
        rect_y = (robot.pos[1]-1) * CELL_SIZE
    elif robot.dir == 'right' and robot.pos[0] < len(maze[0]) - 1:
        rect_x = (robot.pos[0]+1) * CELL_SIZE
        rect_y = robot.pos[1] * CELL_SIZE
    elif robot.dir == 'down' and robot.pos[1] < len(maze) - 1:
        rect_x = robot.pos[0] * CELL_SIZE
        rect_y = (robot.pos[1]+1) * CELL_SIZE
    elif robot.dir == 'left' and robot.pos[0] > 0:
        rect_x = (robot.pos[0]-1) * CELL_SIZE
        rect_y = robot.pos[1] * CELL_SIZE
    else:
        rect_x = robot.pos[0] * CELL_SIZE
        rect_y = robot.pos[1] * CELL_SIZE
    context.fillStyle = GREEN
    context.fillRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

    # Draw the robot
    rect_x = robot.pos[0] * CELL_SIZE
    rect_y = robot.pos[1] * CELL_SIZE
    context.fillStyle = RED
    context.fillRect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

robot = Robot()
draw(robot)

def run_simulation():
    assembly_code = js.document.getElementById("assemblyCode").value
    binary_code = assemble_binary(code_string=assembly_code)
    global cpu, robot
    cpu = CPU(binary_code)
    robot = Robot()
    draw(robot)
    run_step()

def run_step():
    if cpu.pc < len(cpu.program):
        # Execute one CPU instruction
        cpu.exec(
            input_func=robot.get_front_cell_bit,
            output_func=robot.move
        )
        draw(robot)
        # Schedule the next step
        print(dir(pyodide))
        js.setTimeout(pyodide.ffi.create_proxy(run_step), delay * 500)
    else:
        js.alert("Simulation complete!")
        print(f"Result: {cpu.reg.output}")

run_simulation()
