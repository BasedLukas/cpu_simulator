

from alu import ALU
from basic_components import Decoder, Mux8Bit

#initialize registers
registers = {0: [1,0,1,0,1,0,1,0],
             1: [0,0,0,0,0,0,0,0],
             2: [0,0,0,0,0,0,0,0],
             3: [0,0,0,0,0,0,0,0]}
# bus starts empty
bus = {"data": [0,0,0,0,0,0,0,0]}
  


#code (3 MSB)
# 000 = move
# 001 = add
# 010 = subtract
# 011 = and
# 100 = or

# Operands (next 4 MSB for 2 operands)
# 00 = register 0
# 01 = register 2
# 10 = register 3
# 11 = register 4

# destination for arithmetic operations (LSB)
# 0 = register 0
# 1 = register 1

def print_reg():
    print('registers:')
    print(registers[0])
    print(registers[1])
    print(registers[2])
    print(registers[3])
    print()

def move(input1:int, input2:int) -> list[bool]:
    """moves from in1 to in2, placeholder function for moving data from one register to another"""
    global bus
    bus["data"] = registers[input1]
    registers[input2] = bus["data"]

def decode_register(operand:list[bool]) -> int:
    """placeholder function for decoding which register to use
    we later create a logical one"""
    if operand == [False, False]:
        return 0
    elif operand == [False, True]:
        return 1
    elif operand == [True, False]:
        return 2
    elif operand == [True, True]:
        return 3
    else:
        print('error')
        return 0

class Control:
    """takes an instruction byte and decodes it, then executes it"""
    def __init__(self, input:list[bool]):
        self.input = input
        self.decoded = Decoder(self.input).output()
        # next 2 bits are operand1
        self.operand1 = self.input[3:5]
        # next 2 bits are operand2
        self.operand2 = self.input[5:7]
        print('input',self.input)
        print('command',self.input[0:3])
        print('operand1',self.operand1)
        print('operand2',self.operand2)
        print('destination (for arithmetic)',self.input[7])
        print_reg()

        if self.decoded[0] == True:
            """Move from operand1 to operand2"""
            source_register_int = decode_register(self.operand1)
            destination_register_int = decode_register(self.operand2)
            move(source_register_int, destination_register_int)
            print('moved')
        elif self.decoded[1] == True:
            """Add operand1 and operand2, store in reg 1 or 2 depending on last bit"""
            reg1 = decode_register(self.operand1)
            reg2 = decode_register(self.operand2)
            reg1 = registers[reg1]
            reg2 = registers[reg2]
            alu = ALU(reg1, reg2, False, False)
            result = alu.out()
            print('added')
            if self.input[7] == True:
                registers[1] = result
                print('stored in reg 1')
            else:
                registers[0] = result
                print('stored in reg 0')
            
        elif self.decoded[2] == True:
            """Subtract operand1 - operand2, store in reg 1 or 2 depending on last bit"""
            reg1 = decode_register(self.operand1)
            reg2 = decode_register(self.operand2)
            reg1 = registers[reg1]
            reg2 = registers[reg2]
            alu = ALU(reg1, reg2, True, False)
            result = alu.out()
            print('subtracted')
            if self.input[7] == True:
                registers[1] = result
                print('stored in reg 1')
            else:
                registers[0] = result
                print('stored in reg 0')
        elif self.decoded[3] == True:
            """And operand1 and operand2, store in reg 1 or 2 depending on last bit"""
            reg1 = decode_register(self.operand1)
            reg2 = decode_register(self.operand2)
            reg1 = registers[reg1]
            reg2 = registers[reg2]
            alu = ALU(reg1, reg2, True, True)
            result = alu.out()
            print('anded')
            if self.input[7] == True:
                registers[1] = result
                print('stored in reg 1')
            else:
                registers[0] = result
                print('stored in reg 0')
        elif self.decoded[4] == True:
            """Or operand1 and operand2, store in reg 1 or 2 depending on last bit"""
            reg1 = decode_register(self.operand1)
            reg2 = decode_register(self.operand2)
            reg1 = registers[reg1]
            reg2 = registers[reg2]
            alu = ALU(reg1, reg2, False, True)
            result = alu.out()
            print('ored')
            if self.input[7] == True:
                registers[1] = result
                print('stored in reg 1')
            else:
                registers[0] = result
                print('stored in reg 0')
        elif self.decoded[5] == True:
            pass
        elif self.decoded[6] == True:
            pass
        elif self.decoded[7] == True:
            pass
        else:
            print('error')
        print_reg()


#move reg 0 to all registers
instruction1 = [0,0,0,0,0,0,1,1]
instruction2 = [0,0,0,0,0,1,0,1]
instruction3 = [0,0,0,0,0,1,1,1]

# add registers 2 and 3, store in reg 0
instruction4 = [0,0,1,0,1,1,0,0]

program = [[instruction1], [instruction2], [instruction3], [instruction4]]

for instruction in program:

    Control(instruction[0])
