
# 8 bit CPU emulator

This project emulates an 8 bit CPU using simulated logic gates. All the operations and control flow are based on the underlying properties of the logic gates, and changing their operation leads to corresponding changes in function.
For a more thorough explanation see my blog posts [here](https://loreley.one/2023-07-cpu/) and [here](https://loreley.one/2024-12-wasm/).
 
 <img src="./docs/full_cpu.png" width="600">
 
# Usage  
```bash
git clone https://github.com/BasedLukas/cpu_simulator.git
pip install pygame
cd cpu_simulator
python maze_run.py
```
The cpu and assembler themselves have no dependencies.
The maze requires pygame.
Watch the cpu control a robot in a maze. The (red) robot sees one square ahead (green), and is controlled by the `robot.asm` program.  

To interact directly with the cpu and write your own assembly code:
```bash
cd web
pip install wheel
python setup.py bdist_wheel
python -m http.server
```
Visit localhost:8000 to write your own assembly code in the browser. Can you solve the maze? 

![](./docs/maze.gif)  

  
# Coding
### Introduction

This CPU features six general-purpose registers (`reg0` to `reg5`), along with a special register (`reg6`) used for both input and output. It supports four main types of operations:

- **Immediate Values**
- **Arithmetic Operations**
- **Copying**
- **Comparisons and Control Flow**

All values in the CPU are 8-bit and overflow after 255 to 0. 
For comparisons, values are treated as **signed** (range -128 to 127).

---

### Immediate Values

Load a constant value into `reg0`. Only values up to 63 are allowed because the two most significant bits (MSB) are reserved for instruction encoding.

```
0       # Load 0 into reg0 (min allowed immediate)
36      # Load 36 into reg0
63      # Load 63 into reg0 (max allowed immediate)
```

---

### Copying Data

The `copy` instruction copies data between registers or between a register and the input/output.
**Input and Output**: `reg6` serves as both the input and output register.

```
copy <source_register> <destination_register>
``` 
```
copy 6 1   # Copy value from input (reg6) to reg1
copy 3 6   # Copy value from reg3 to output (reg6)
copy 5 3   # Copy value from reg5 into reg3
copy 6 6   # Copy from input directly to output
copy 1 1   # NOP
```

---

### Arithmetic and Logical Operations

Arithmetic and logical operations use `reg1` and `reg2` as operands and store the result in `reg3`. Supported operations:
Arithmetic uses 2's complliment. Values overflow if they exceed 255. 

**Addition** (`add`): Adds `reg1` and `reg2`.
**Subtraction** (`sub`): Subtracts `reg2` from `reg1`.
**Bitwise AND** (`and`): Performs a bitwise AND operation on `reg1` and `reg2`.
**Bitwise OR** (`or`): Performs a bitwise OR operation on `reg1` and `reg2`.


```
1        # Load 1 into reg0
copy 0 1 # Move 1 into reg1
2        # Load 2 into reg0
copy 0 2 # Move 2 into reg2
add      # reg3 = reg1 + reg2 = 1 + 2 = 3
copy 3 6 # Output result (3)
```

```
32
copy 0 1
32
copy 0 2
add  # 64 in reg 3
copy 3 2
copy 3 1
add # 128 in reg 3
copy 3 1
copy 3 2
add 
copy 3 6
# total 256, so output is 0 == [0,0,0,0,0,0,0,0]
```

```
0
copy 0 1
2
copy 0 2
sub  # 0 - 2 = -2
copy 3 6
# cpu output is -2 == [1,1,1,1,1,1,1,0]
```

```
32
copy 0 1
32
copy 0 2
add  # 64 in reg 3
copy 3 2
copy 3 1
add # 128 in reg 3
1
copy 0 2
copy 3 1
sub     # 128 - 1
copy 3 6
# result is 127 == [0,1,1,1,1,1,1,1] in 2's compliment
```

---

### Comparisons and Control Flow

The `eval` instruction compares the **signed** value in `reg3` against `0`. If the condition is true, the program counter jumps to the address in `reg0`.

```
eval <condition>
```

Supported conditions:

- `eval always`: Always jump.
- `eval never`: Never jump.
- `eval =`: Jump if `reg3 == 0`.
- `eval !=`: Jump if `reg3 != 0`.
- `eval <`: Jump if `reg3 < 0` (signed).
- `eval <=`: Jump if `reg3 <= 0` (signed).
- `eval >`: Jump if `reg3 > 0` (signed).
- `eval >=`: Jump if `reg3 >= 0` (signed).

---

### Labels

Labels act as named locations in the program. Defining a label associates it with its position in the program. Calling labels is just shorthand for using immediate values (and thus labels can't be placed after line 63).


```
label <name>
```
```
label start # start = 0
copy 6 1    # Read input into reg1
add         # Add reg1 and reg2
start       # Label used here as jump target, equvalent to using immediate 0
eval >=     # Jump to "start" if reg3 >= 0
```

This program copies `1` into `reg1`, adds it with `reg2`, and stores the result in `reg2` in a loop until the result overflows and becomes negative.

```
1           # Load 1 into reg0
copy 0 1    # Copy 1 into reg1
label loop
add         # reg3 = reg1 + reg2
copy 3 2    # Store result in reg2
copy 3 6    # print result to output
loop
eval >=     # Jump to label loop if reg3 >= 0
```

**For comparisons, the value is treated as signed (`127` is interpreted as `127`, but `128` is interpreted as `-128`). The last result the cpu prints is thus `128`**

### Robot Instructions

output (controls):
`1 == turn left`  
`2 == turn right`  
`3 == step forward`

input:
`1 == wall`  
`0 == clear`

```
# this will rotate you left
1
copy 0 6

# rotate right 3 times
2
copy 0 6
copy 0 6
copy 0 6

# walk in a line until blocked
label start_loop
3
copy 0 6
copy 6 3    # put the input in reg3
start_loop
eval =      # if reg3 is 0 there is no wall
```



#### Modifying

To write input and read output from the CPU pass it in as a callable.  
```
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
```

