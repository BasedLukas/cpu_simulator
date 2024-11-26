from maze import Robot, draw
from hardware.new_cpu import CPU
from assembler.assembler import assemble_binary


if __name__ == "__main__":
    robot = Robot()
    program = assemble_binary('robot.asm')
    cpu = CPU(program)
    cpu.run(
        write_to_input=robot.get_front_cell_bit,
        read_from_output=robot.move
    )


