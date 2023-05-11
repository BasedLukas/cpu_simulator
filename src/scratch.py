

from alu import ALU
from basic_components import Decoder, Mux8Bit



def move(input1:list[bool], input2:list[bool]) -> list[bool]:
    """moves the data from input1 to input2"""
    mux = Mux8Bit(input1, input2, True)
    return mux.output()

class Control:
    def __init__(self, input:list[bool]):
        # first 3 bits are the opcode, decoder will automatically chop them off
        self.input = input
        self.decoded = Decoder(self.input).output()
        # next 2 bits are operand1
        self.operand1 = self.input[3:5]
        # next 2 bits are operand2
        self.operand2 = self.input[5:7]
        print(self.input)
        print(self.decoded)
        print(self.operand1)
        print(self.operand2)

        # now we need to use the decoder to determine what to do
        # if the opcode is 000 then we need to move the data from register1 to register2
        # if the opcode is 001 then we need to add register1 and register2
        # if the opcode is 010 then we need to subtract register1 and register2
        # if the opcode is 011 then we need to and register1 and register2
        # if the opcode is 100 then we need to or register1 and register2

        if self.decoded[0] == True:
            move(register1, register2)
        elif self.decoded[1] == True:
            pass
        elif self.decoded[2] == True:
            pass
        elif self.decoded[3] == True:
            pass
        elif self.decoded[4] == True:
            pass
        elif self.decoded[5] == True:
            pass
        elif self.decoded[6] == True:
            pass
        elif self.decoded[7] == True:
            pass



  # Define registers and bus as dictionaries
registers = {"R1": [True, False, True, False, True, False, True, False],
             "R2": [False, False, False, False, False, False, False, False]}
bus = {"data": [False, False, False, False, False, False, False, False]}
  
# Define instruction
instruction = [False, False, False, True, False, False, False, True]

Control(instruction)
