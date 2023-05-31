from maze import Robot, draw
import pygame
import sys
from hardware.cpu import CPU
from assembler import assemble_binary
import time


robot = Robot()
program = assemble_binary('robot.asm')
cpu = CPU(program)
cpu.run(write_to_input=robot.get_front_cell_bit,read_from_output=robot.move)


