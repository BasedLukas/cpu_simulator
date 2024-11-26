from .gates import and_, or_, not_
from .basic_components import decode, control, comparison
from .alu import alu
from .registers import Registers


class CPU:
    """
    A simple CPU simulation with a custom instruction set.

    Instruction Set:
        - 00: Immediate
            WARNING: max val == 63 (to preserve upper 2 MSB)
            Moves an 6-bit immediate value into register 0.
            Example:
                00 000 000: Move 0 into reg0
                00 000 001: Move 1 into reg0

        - 01: Operate (Add, Subtract, AND, OR)
            Performs an ALU operation on reg1 and reg2, stores the result in reg3.
            ALU Control Bits:
                control1 | control2 | Operation
                ---------|----------|-----------
                0        | 0        | Add
                0        | 1        | OR
                1        | 0        | Subtract
                1        | 1        | AND

        - 10: Copy (Source, Destination)
            Copies data from a source to a destination register or I/O.
            Register Codes:
                000-101: Registers 0-5
                110: Input or Output

            Examples:
                10 000 010: Move from reg0 to reg2
                10 000 110: Move from reg0 to output
                10 110 000: Move from input to reg0

        - 11: Update Program Counter / Evaluate Comparison
            Updates the program counter to the value in reg0 if a comparison is true.
    """

    def __init__(self, program):
        self.program = program
        self.pc = 0  # Program Counter
        self.reg = Registers()  # Registers and I/O
        self.alu = None

    def exec(self, input_func=None, output_func=None):
        # Reset load and save signals
        self.reg.load = [0] * 6
        self.reg.save = [0] * 6
        self.reg.input_load = 0
        self.reg.output_save = 0

        # Clear input and output each cycle
        self.reg.input = [0] * 8
        self.reg.output = [0] * 8

        # Fetch input if provided
        if input_func:
            self.reg.input = input_func()

        # Fetch instruction and increment program counter
        instruction_byte = self.program[self.pc]
        self.pc += 1

        # Decode instruction
        ctl = control(instruction_byte)
        decoder1 = decode(instruction_byte[2:5])  # Source (Load)
        decoder2 = decode(instruction_byte[5:8])  # Destination (Save)

        # Immediate Instruction
        self.reg.save[0] = ctl[0]  # Enable save to reg0 if immediate instruction
        self.reg.write(instruction_byte)  # Write immediate value to reg0

        # Operate Instruction
        # ALU is connected to reg1 and reg2; no need to set load/save signals
        alu_result = alu(
            self.reg.registers[1],
            self.reg.registers[2],
            instruction_byte[6],
            instruction_byte[7],
        )
        self.alu = alu_result
        alu_out = alu_result.out
        self.reg.save[3] = ctl[1]  # Enable save to reg3 if operate instruction
        self.reg.write_to_register(3, alu_out)  # Write ALU output to reg3

        # Copy Instruction
        # Set load and save signals based on control signals and decoders
        self.reg.load = [
            or_(and_(ctl[2], decoder1[i]), and_(ctl[3], i == 3)) for i in range(6)
        ]
        self.reg.save = [and_(ctl[2], decoder2[i]) for i in range(6)]
        self.reg.input_load = and_(ctl[2], decoder1[6])  # Load from input
        self.reg.output_save = and_(ctl[2], decoder2[6])  # Save to output

        # Read from source and write to destination
        data = self.reg.read()
        self.reg.write(data)

        # Compare Instruction
        # Perform comparison and update program counter if necessary
        compare_result = comparison(control=instruction_byte, byte=data)
        update_counter = int(and_(ctl[3], compare_result))
        reg0_value = int("".join(str(int(x)) for x in self.reg.registers[0]), 2)
        self.pc = (1 - update_counter) * self.pc + update_counter * reg0_value

        # Provide output if output function is given
        if output_func:
            output_func(self.reg.output)

    def run(self, write: callable = None, read: callable = None):
        """write: function to write to the cpu input
        read: function to read from cpu output"""
        while self.pc < len(self.program):
            self.exec(write, read)
