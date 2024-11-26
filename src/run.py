from hardware.cpu import CPU
from assembler.assembler import assemble_binary


program = assemble_binary("program.asm")



# Function to read output from the CPU
def print_result(value):
    # Convert binary list to integer and print result
    result = int(''.join(map(str, value)), 2)
    if result != 0:
        print('Result:', result)

# Initialize and run the CPU
cpu = CPU(program)
cpu.run(read=print_result)
