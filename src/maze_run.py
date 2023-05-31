from maze import Robot, draw
import pygame
import sys
from cpu import CPU
from assembler import assemble_binary
import time

robot = Robot([1,1], 'up')

cpu = CPU(assemble_binary('robot.asm'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        draw(robot)
        time.sleep(1)
        cpu.run(write_to_input=robot.get_front_cell_bit,read_from_output=robot.move)
        time.sleep(1)
        pygame.quit()
        sys.exit()
