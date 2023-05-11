
from alu import ALU


# programming the cpu
# 1 == add == 00
# 2 == subtract == 10
# 3 == logical and == 11
# 4 == logical or == 01

program = [

    1,  # add
    2,  # subtract
    3,  # logical and
    4,  # logical or
]

register1 = [True, True, True, True, False, False, False, False]
register2 = [True, False, True, False, True, False, True, False]

language = { 1: [False,False], 2: [True, False], 3: [True,True], 4: [False,True] }

# high level cpu for testing purposes
class CPU:
    def __init__(self, program, register1, register2):
        self.program = program
        self.pc = 0  # Program Counter
        self.register1 = register1
        self.register2 = register2

    def fetch(self):
        instruction = self.program[self.pc]
        self.pc += 1
        return instruction

    def decode(self, instruction):
        return language[instruction][0] , language[instruction][1]

    def execute(self):
        instruction = self.fetch()
        opcode1, opcode2 = self.decode(instruction)
        alu = ALU(register1, register2, opcode1, opcode2)
        return alu

    def run(self):
        while self.pc < len(self.program):
            alu = self.execute()
            output = alu.out()
            # convert registers to decimal
            register1_dec = int("".join([str(int(x)) for x in register1]), 2)
            register2_dec = int("".join([str(int(x)) for x in register2]), 2)
           # convert output to decimal
            output_dec = int("".join([str(int(x)) for x in output]), 2)
            print(f"register1: {register1_dec}, register2: {register2_dec}, output: {output_dec}")





cpu = CPU(program, register1, register2)
cpu.run()

