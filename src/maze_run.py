from maze import Robot, draw
from hardware.new_cpu import CPU
from assembler import assemble_binary


robot = Robot()
program = assemble_binary('robot.asm')
cpu = CPU(program)
#draw(robot,delay=1)
cpu.run(write_to_input=robot.get_front_cell_bit,read_from_output=robot.move)


