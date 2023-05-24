

from alu import ALU
from basic_components import Decoder, Mux8Bit, Control

"""

Instruction set
00 = Immediate
01 = operate (add, subtract, and, or)
10 = copy
11 = undefined TODO

IMMEDIATE:
moves the number into reg0, example:
00 000 000 = move 0 into reg0
00 000 001 = move 1 into reg0
notice that the 2 MSB must always be false

OPERATE:
2 LSB determine operation as per alu specs
always operates on reg1 and reg2 and stores in reg3

COPY:
3 bits determine source register, next 3 bits determine destination register. 
110 refers to input or output


10 000 010 = move from reg0 to reg2
10 000 110 = move from reg0 to out 
10 110 000 = move from in to reg0
"""


#initialize registers
registers = {0: [0,0,0,0,0,0,0,0],
             1: [0,0,0,0,0,0,0,0],
             2: [0,0,0,0,0,0,0,0],
             3: [0,0,0,0,0,0,0,0],
             4: [0,0,0,0,0,0,0,0],
             5: [0,0,0,0,0,0,0,0],}

# bus starts empty
bus = {"data": [0,0,0,0,0,0,0,0]}

program = [
     # MOVE 3 into reg0
   [0,0,0,0,0,0,1,1],
   # copy into reg 1
    [1,0,0,0,0,0,0,1],
    #move 5 into reg0
    [0,0,0,0,0,1,0,1],
    #copy into reg2
    [1,0,0,0,0,0,1,0],
    #add reg1 and reg2 and store in reg3
    [0,1,0,0,0,0,0,0],

]


def print_reg():
    print('registers:')
    print('reg0',registers[0])
    print('reg1',registers[1])
    print('reg2',registers[2])
    print('reg3',registers[3])
    print('reg4',registers[4])
    print('reg5',registers[5])
    print()

""""we need a way to move from one of 6 locations to another of 6 locations
we can use a 3 bit decoder to select the source and destination
we need a 2 bit decoder to select the operation"""

# the incoming program is attached to the control and 2 decoders

class CPU:
    def __init__(self, program_instruction_byte):
        self.program_instruction_byte = program_instruction_byte
        self.control = Control(self.program_instruction_byte)
        self.decoder1 = Decoder(self.program_instruction_byte[2:5])
        self.decoder2 = Decoder(self.program_instruction_byte[5:8])

        print('instruction byte',self.program_instruction_byte)
        print_reg()
        # when operation is immediate, we need to move the 8 bits into reg0
    
    def execute(self):
        
        if self.control.output[0]:
            print('immediate')
            registers[0] = self.program_instruction_byte
            
        elif self.control.output[1]:
            self.alu = ALU(registers[1], registers[2], self.program_instruction_byte[6], self.program_instruction_byte[7])
            print('operate')
            registers[3] = self.alu.out

        elif self.control.output[2]:
            print('copy')
            source_reg = self.decoder1.output
            destination_reg = self.decoder2.output
            # use output of decoder to select source
            if source_reg[0]:
                # source is reg0
                print('source is reg0')
                source = registers[0]
            elif source_reg[1]:
                # source is reg1
                print('source is reg1')
                source = registers[1]
            elif source_reg[2]:
                # source is reg2
                print('source is reg2')
                source = registers[2]
            elif source_reg[3]:
                # source is reg3
                print('source is reg3')
                source = registers[3]
            elif source_reg[4]:
                # source is reg4
                print('source is reg4')
                source = registers[4]
            elif source_reg[5]:
                # source is reg5
                print('source is reg5')
                source = registers[5]
            else:
                pass
                # source is input
                #TODO implement input
            # use output of decoder to select destination
            if destination_reg[0]:
                # destination is reg0
                print('destination is reg0')
                registers[0] = source
            elif destination_reg[1]:
                # destination is reg1
                print('destination is reg1')
                registers[1] = source
            elif destination_reg[2]:
                # destination is reg2
                print('destination is reg2')
                registers[2] = source
            elif destination_reg[3]:
                # destination is reg3
                print('destination is reg3')
                registers[3] = source
            elif destination_reg[4]:
                # destination is reg4
                print('destination is reg4')
                registers[4] = source
            elif destination_reg[5]:
                # destination is reg5
                print('destination is reg5')
                registers[5] = source
            else:
                pass
                # destination is output
                #TODO implement output
            
        
        
        
        print_reg()




for i in range(len(program)):
            
    CPU(program[i]).execute()