
from .gates import and_, or_, not_, nand, nor, xor, xnor

class HalfAdder:
    def __init__(self, input1:bool, input2:bool):
        self.input1 = input1
        self.input2 = input2
    
    def sum(self) -> bool:
        return xor(self.input1, self.input2)
 
    def carry(self)->bool:
        return and_(self.input1, self.input2)
    

class FullAdder:
    def __init__(self, input1:bool, input2:bool, carry_in:bool):
        self.input1 = input1
        self.input2 = input2
        self.carry_in = carry_in
        self.half_adder1 = HalfAdder(input1, input2)
        self.half_adder2 = HalfAdder(self.half_adder1.sum(), carry_in)

    def sum(self):
        return self.half_adder2.sum()
    
    def carry(self):
        return or_(self.half_adder1.carry(), self.half_adder2.carry())
    

class Adder:
    def __init__(self, input1: list[bool], input2: list[bool], carry_in: bool = False):
        if len(input1) != 8 or len(input2) != 8:
            raise ValueError("Both inputs must be 8 bits long.")
        
        self.input1 = input1
        self.input2 = input2
        self.full_adders = []

        # Process the bits from right to left (LSB to MSB)
        for bit1, bit2 in zip(reversed(self.input1), reversed(self.input2)):
            full_adder = FullAdder(bit1, bit2, carry_in)
            self.full_adders.append(full_adder)
            carry_in = full_adder.carry()

    def sum(self) -> list[bool]:
        # Reverse the sum result to get the correct order of bits (MSB to LSB)
        return list(reversed([full_adder.sum() for full_adder in self.full_adders]))

    def carry_out(self) -> bool:
        return self.full_adders[-1].carry()


class HalfSubtractor:
    #Important: Order of connections matters; input 1 - input2
    def __init__(self, input1:bool, input2:bool):
        self.input1 = input1
        self.input2 = input2
    
    def diff(self) -> bool:
        return xor(self.input1, self.input2)
 
    def borrow(self)->bool:
        return and_(not_(self.input1), self.input2)
    

class FullSubtractor:
    #TODO add test
    def __init__(self, input1:bool, input2:bool, borrow_in:bool):
        self.input1 = input1
        self.input2 = input2
        self.borrow_in = borrow_in
        self.half_subtractor1 = HalfSubtractor(input1, input2)
        self.half_subtractor2 = HalfSubtractor(self.half_subtractor1.diff(), borrow_in)

    def diff(self):
        return self.half_subtractor2.diff()
    
    def borrow(self):
        return or_(self.half_subtractor1.borrow(), self.half_subtractor2.borrow())
    

class Subtractor:
    def __init__(self, input1: list[bool], input2: list[bool], borrow_in: bool = False):
        if len(input1) != 8 or len(input2) != 8:
            raise ValueError("Both inputs must be 8 bits long.")
        
        self.input1 = input1
        self.input2 = [not_(x) for x in input2]  # invert input2
        self.carry_in = not_(borrow_in)  # carry_in is the inverse of borrow_in

        self.adder = Adder(self.input1, self.input2, self.carry_in)

    def diff(self) -> list[bool]:
        return self.adder.sum()
        
    def borrow_out(self) -> bool:
        return not self.adder.carry_out()  # borrow_out is the inverse of carry_out


class Mux:
    """True = 1, False = 2"""
    def __init__(self, input1:bool, input2:bool, sel:bool):
        self.input1 = input1
        self.input2 = input2
        self.sel = sel
    
    def output(self) -> bool:
        nand_central = nand(self.sel, self.sel)
        nand1 = nand(self.input1, self.sel)
        nand2 = nand(self.input2,nand_central)
        output = nand(nand1, nand2)
        return output


class Mux8Bit:
    """True = 1, False = 2"""
    def __init__(self, input1:list[bool], input2:list[bool], sel:bool):
        assert len(input1) == 8 and len(input2) == 8, "Inputs should be 8 bits."
        self.input1 = input1
        self.input2 = input2
        self.sel = sel
    
    def output(self) -> list[bool]:
        output = []
        for bit1, bit2 in zip(self.input1, self.input2):
            nand_central = nand(self.sel, self.sel)
            nand1 = nand(bit1, self.sel)
            nand2 = nand(bit2,nand_central)
            output_bit = nand(nand1, nand2)
            output.append(output_bit)
        return output
        

class AddSub:
    """
    input1 - input2
    if operation == True then subtract else add
    overflow used when doing addition
    borrow out used when doing subtraction (in2 > in1))"""
    def __init__(self, input1: list[bool], input2: list[bool], operation: bool):
        self.input1 = input1
        # we need to xor input 2 with operation
        self.input2 = [xor(x, operation) for x in input2] 
        self.operation = operation

        self.adder = Adder(self.input1, self.input2, self.operation)
    
    def output(self) -> list[bool]:
        return self.adder.sum()
    def overflow(self) -> bool:
        """used when doing addition"""
        return self.adder.carry_out()
    def  borrow_out(self) -> bool:
        """used when doing subtraction"""
        return not_(self.adder.carry_out())


# class Decoder:
#     """3 bit decoder, uses the 3 MSB in the input
#     output is a list of 8 bits where 0 is MSB and 7 is LSB"""

#     def __init__ (self, input:list[bool]):
#         self.input = input[:3]
#         self.output_list = [0]*8
#         self.output_list[0] = and_(not_(self.input[0]), not_(self.input[1]), not_(self.input[2]))
#         self.output_list[1] = and_(not_(self.input[0]), not_(self.input[1]), self.input[2])
#         self.output_list[2] = and_(not_(self.input[0]), self.input[1], not_(self.input[2]))
#         self.output_list[3] = and_(not_(self.input[0]), self.input[1], self.input[2])
#         self.output_list[4] = and_(self.input[0], not_(self.input[1]), not_(self.input[2]))
#         self.output_list[5] = and_(self.input[0], not_(self.input[1]), self.input[2])
#         self.output_list[6] = and_(self.input[0], self.input[1], not_(self.input[2]))
#         self.output_list[7] = and_(self.input[0], self.input[1], self.input[2])
    
#     @property
#     def output(self) -> list[bool]:
#         return self.output_list

from .gates import and_, not_

def decode(bits: list[bool]) -> list[bool]:
    """
    3-Bit Decoder Function.

    Uses 3 bits from the input to produce an 8-bit output where only one bit is True,
    corresponding to the decoded value. The output is a list of 8 bits where index 0 is the MSB and index 7 is the LSB.

    Args:
        input_bits (list[bool]): Input list of bits.

    Returns:
        list[bool]: An 8-bit output list representing the decoded value.

    Raises:
        ValueError: If the input_bits list doesnt have 3 bits.
    """
    if len(bits) != 3:
        raise ValueError("Input must have at 3 bits.")
    


    # Initialize output list
    output_list = [False] * 8

    # Compute the output bits
    output_list[0] = and_(not_(bits[0]), not_(bits[1]), not_(bits[2]))
    output_list[1] = and_(not_(bits[0]), not_(bits[1]), bits[2])
    output_list[2] = and_(not_(bits[0]), bits[1], not_(bits[2]))
    output_list[3] = and_(not_(bits[0]), bits[1], bits[2])
    output_list[4] = and_(bits[0], not_(bits[1]), not_(bits[2]))
    output_list[5] = and_(bits[0], not_(bits[1]), bits[2])
    output_list[6] = and_(bits[0], bits[1], not_(bits[2]))
    output_list[7] = and_(bits[0], bits[1], bits[2])

    return output_list



# class Control:
#     """2 bit decoder to determine the operation of the CPU
#     uses 2 MSB
#     has 4 outputs for 4 different operations
#     00 = Immediate
#     01 = operate (add, subtract, and, or)
#     10 = copy
#     11 = update
    
#     output[0] = 00
#     output[1] = 01
#     output[2] = 10
#     output[3] = 11
#     """

#     def __init__(self, input:list[bool]):
#         self.input = input[:2]
#         self.output_list = [0]*4
#         self.output_list[0] = and_(not_(self.input[0]), not_(self.input[1])) # 00
#         self.output_list[1] = and_(not_(self.input[0]), self.input[1]) # 01
#         self.output_list[2] = and_(self.input[0], not_(self.input[1])) # 10
#         self.output_list[3] = and_(self.input[0], self.input[1]) # 11

#     @property
#     def output(self) -> list[bool]:
#         return self.output_list
    

def control(input_bits: list[bool]) -> list[bool]:
    """
    2-Bit Decoder Function for CPU Operation Control.

    Uses the 2 most significant bits (MSB) from the input to produce a 4-bit output where only one bit is True,
    corresponding to the operation code. The output corresponds to the following operations:

        00 = Immediate
        01 = Operate (add, subtract, and, or)
        10 = Copy
        11 = Update

    The output list is as follows:
        output[0] = True if operation is 00 (Immediate)
        output[1] = True if operation is 01 (Operate)
        output[2] = True if operation is 10 (Copy)
        output[3] = True if operation is 11 (Update)

    Args:
        input_bits (list[bool]): Input list of bits. Only the first 2 bits (MSB) are used.

    Returns:
        list[bool]: A 4-bit output list representing the control signals for CPU operations.

    Raises:
        ValueError: If the input_bits list has fewer than 2 bits.
    """
    if len(input_bits) < 2:
        raise ValueError("Input must have at least 2 bits.")

    # Use the first 2 bits (MSB)
    bits = input_bits[:2]

    # Compute the control outputs
    output_list = [
        and_(not_(bits[0]), not_(bits[1])),  # 00 - Immediate
        and_(not_(bits[0]), bits[1]),        # 01 - Operate
        and_(bits[0], not_(bits[1])),        # 10 - Copy
        and_(bits[0], bits[1]),              # 11 - Update
    ]

    return output_list

# class Comparison:
#     """
#     Takes 3 control bits, and a byte to be evaluated and returns boolean based on comparison
#     USES SIGNED NUMBERS 10000000 = -128
#     cntrl | byte value | output
#     ___________________________
#     000   | any        | false
#     001   | =0         | true
#     010   | <0         | true
#     011   | <=0        | true
#     100   | any        | true
#     101   | !=0        | true
#     110   | >=0        | true
#     111   | >0         | true
#     """
#     def __init__(self, control:list[bool], byte:list[bool]):
#         """check docs to understand design,
#         byte[0] is MSB, control[0] is MSB"""
#         self.control = control[-3:]
#         self.byte = byte
#         self.nor = nor(*byte) # if all bits are 0, nor will be 1
#         self.switch1 = and_(self.control[1], self.byte[0]) 
#         self.switch2 = and_(self.control[2], self.nor)
#         self.or1 = or_(self.switch1, self.switch2)
#         self.xor = xor(self.control[0], self.or1)

    
#     @property
#     def out(self) -> bool:
#         return self.xor



def comparison(control: list[bool], byte: list[bool]) -> bool:
    """
    Evaluates a byte against specified conditions based on control bits and returns a boolean result.

    Uses signed numbers (two's complement representation, where 10000000 represents -128).

    Control bits correspond to different comparison conditions:

        cntrl | byte value | output
        ---------------------------
        000   | any        | False
        001   | == 0       | True
        010   | < 0        | True
        011   | <= 0       | True
        100   | any        | True
        101   | != 0       | True
        110   | >= 0       | True
        111   | > 0        | True

    Args:
        control (list[bool]): List of 3 control bits (control[0] is MSB).
        byte (list[bool]): List of 8 bits representing the byte to be evaluated (byte[0] is MSB).

    Returns:
        bool: The result of the comparison based on the control bits and byte value.

    Raises:
        ValueError: If the control list does not have exactly 3 bits or the byte list does not have exactly 8 bits.
    """
    # if len(control) <= 3:
    #     raise ValueError("Control must be a list of exactly 3 bits.")
    # if len(byte) != 8:
    #     raise ValueError("Byte must be a list of exactly 8 bits.")

    # Extract control bits (ensure they are the last 3 bits)
    control_bits = control[-3:]

    # Calculate the NOR of all bits in the byte
    nor_byte = nor(*byte)  # True if all bits in byte are False (i.e., byte == 0)

    # Determine if the byte is negative (byte[0] is MSB)
    is_negative = byte[0]

    # Compute switch1 and switch2 based on control bits and byte value
    switch1 = and_(control_bits[1], is_negative)
    switch2 = and_(control_bits[2], nor_byte)

    # Compute or1 as the OR of switch1 and switch2
    or1 = or_(switch1, switch2)

    # Compute the final output using XOR with control_bits[0]
    output = xor(control_bits[0], or1)

    return output