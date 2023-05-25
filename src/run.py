from cpu import CPU
from assembler import assemble_binary


program = assemble_binary('program.asm')
print(program)


cpu = CPU(program)
cpu.run()
