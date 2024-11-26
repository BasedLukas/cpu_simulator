from hardware.new_cpu import CPU
from assembler.assembler import assemble_binary


program = assemble_binary("program.asm")

# Input values for each cycle
input_values = iter([
    [0, 0, 0, 0, 0, 0, 0, 1],  # Input 1
    [0, 0, 0, 0, 0, 0, 1, 0],  # Input 2
    [0, 0, 0, 0, 0, 0, 1, 1],  # Input 3
    [0, 0, 0, 0, 0, 1, 0, 0],  # Input 4
    [0, 0, 0, 0, 0, 1, 0, 1],  # Input 5
])

# Function to provide input to the CPU
def write_to_input():
    return next(input_values, [0] * 8)  # Provide input or all-zeroes if no input remains

# Function to read output from the CPU
def read_from_output(value):
    # Convert binary list to integer and print result
    result = int(''.join(map(str, value)), 2)
    print('Result:', result)

# Initialize and run the CPU
cpu = CPU(program)
cpu.run(write_to_input, read_from_output)
