import os
from hardware.cpu import CPU
from assembler.assembler import assemble_binary

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
relative_path = os.path.join(current_dir, "program.asm")
program = assemble_binary(relative_path)



# Function to read output from the CPU
def print_result(value):
    print(value)
    # Convert binary list to integer and print result
    result = int(''.join(map(str, value)), 2)
    if result != 0:
        print('Result:', result)

# Initialize and run the CPU
cpu = CPU(program)
cpu.run(read=print_result)
