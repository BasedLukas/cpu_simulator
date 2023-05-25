
from cpu import CPU
from assembler import assemble_binary


program = assemble_binary('program.asm')



cpu = CPU(program)
cpu.run()
