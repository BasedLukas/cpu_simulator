
import pygame
import os

from hardware.cpu import CPU
from assembler.assembler import assemble_binary
from maze.game import Robot, maze, CELL_SIZE




def run_maze():
    pygame.init()
    window = pygame.display.set_mode((len(maze[0])*CELL_SIZE, len(maze)*CELL_SIZE))
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    relative_path = os.path.join(current_dir, "robot.asm")
    robot = Robot(pygame=pygame, window=window)
    program = assemble_binary(relative_path)
    cpu = CPU(program)
    cpu.run(
        write=robot.get_front_cell_bit,
        read=robot.move
    )


