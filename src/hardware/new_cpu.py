from .gates import  and_
from .basic_components import  decode, control, comparison
from .alu import  alu
from .registers import Registers


class CPU:     
    """
    Instruction set
    00 = Immediate
    01 = operate (add, subtract, and, or)
    10 = copy (source, destination)
    11 = Edit program counter/ evaluate comparison

    IMMEDIATE:
    moves the number into reg0, example:
    00 000 000 = move 0 into reg0
    00 000 001 = move 1 into reg0
    notice that the 2 MSB must always be false

    OPERATE:
    2 LSB determine operation as per alu specs
    always operates on reg1 and reg2 and stores in reg3
    ALU rules;
        control1 | control2
        0        | 0        = Add
        0        | 1        = Or
        1        | 0        = Subtract
        1        | 1        = And

    COPY:
    3 bits determine source register, next 3 bits determine destination register. 
    110 refers to input or output

    10 000 010 = move from reg0 to reg2
    10 000 110 = move from reg0 to out 
    10 110 000 = move from input to reg0

    UPDATE PC:
    Update the pc to the value in reg0 if comparison is true
    """
    def __init__(self, program):
        self.program = program
        self.pc = 0
        self.reg = Registers()

    def exec(self, input_func, output_func):
        # Reset load and save signals
        self.reg.load = [0] * 6
        self.reg.save = [0] * 6
        self.reg.input_load = 0
        self.reg.output_save = 0
        #each cycle clear i/o
        self.reg.input = [0] * 8
        self.reg.output = [0] * 8
        if input_func:
            self.reg.input = input_func()

        instruction_byte = self.program[self.pc]
        self.pc += 1
        ctl = control(instruction_byte)
        decoder1 = decode(instruction_byte[2:5])
        decoder2 = decode(instruction_byte[5:8])

        #immediate
        if ctl[0]:
            self.reg.save[0] = ctl[0]
            self.reg.write(instruction_byte)
        # operate
        if ctl[1]:
            #The ALU is permanently connected to the first two registers, so we don't set the load and save signals
            alu_out = alu(self.reg.registers[1], self.reg.registers[2],instruction_byte[6],instruction_byte[7]).out
            # activate reg3 save signal
            self.reg.save[3] = ctl[1]
            self.reg.write(alu_out)
        #copy
        if ctl[2]:
            # Set the save and load signals for the registers
            self.reg.load = decoder1[:6]
            self.reg.save = decoder2[:6]
            self.reg.input_load = decoder1[6]
            self.reg.output_save = decoder2[6]
            # Read from the source registers and write to the destination registers
            data = self.reg.read()
            self.reg.write(data)
        #compare
        if ctl[3]:
            #enable reg3 load
            self.reg.load[3] = ctl[3]
            compare = comparison(control=instruction_byte, byte=self.reg.read())
            update_counter = compare
            if and_(ctl[3], update_counter):
                # get int value of reg0
                reg0 = int(''.join(str(x) for x in self.reg.registers[0]), 2)
                self.pc = reg0

        if output_func: output_func(self.reg.output)

    def run(self, write_to_input:callable=None, read_from_output:callable=None):
        while self.pc < len(self.program):
            self.exec(write_to_input, read_from_output)






