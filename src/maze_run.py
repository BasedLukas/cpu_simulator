from maze import Robot
from hardware.cpu import CPU
from assembler.assembler import assemble_binary


if __name__ == "__main__":
    robot = Robot()
    program = assemble_binary('robot.asm')
    cpu = CPU(program)
    cpu.run(
        write=robot.get_front_cell_bit,
        read=robot.move
    )


