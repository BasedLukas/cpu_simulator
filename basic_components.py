
from gates import and_, or_, not_, nand, nor, xor, xnor

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

tofix: mux doesn't work with lists
class ALU:
    """"
ALU rules;
    control1 | control2
    0        | 0        = Add
    0        | 1        = Or
    1        | 0        = Subtract
    1        | 1        = And

    input1 - input2 = output   
    zero() = True if all the output is False
    negative() = True if the number is negative
    overflow() = True if the number is overflowed when doing addition
    carry_out() = True if the number is overflowed when doing subtraction (in2 > in1) 
        """
    def __init__(self, input1: list[bool], input2: list[bool], control1:bool, control2:bool):
        if len(input1) != 8 or len(input2) != 8:
            raise ValueError("Both inputs must be 8 bits long.")
        self.input1 = input1
        self.input2 = input2
        self.control1 = control1
        self.control2 = control2
    
        # create add sub
        add_sub = AddSub(self.input1, self.input2, self.control1)
        add_sub_out = add_sub.output() # if control1 == True then subtract else add
        add_sub_overflow = add_sub.overflow() # used when doing addition
        add_sub_borrow_out = add_sub.borrow_out() # used when doing subtraction (in2 > in1)


        #create bitwise operations
        and_out = [and_(in1, in2) for in1, in2 in zip(self.input1, self.input2)]
        or_out = [or_(in1, in2) for in1, in2 in zip(self.input1, self.input2)]

        #pass and or output to mux
        and_or_mux = Mux(and_out, or_out, self.control1)
        and_or_mux_out = and_or_mux.output()

        #pass and or mux out + add sub out to mux
        and_or_add_sub_mux = Mux(and_or_mux_out, add_sub_out, self.control2)

    def out(self):
        """returns the output of the ALU"""
        return self.and_or_add_sub_mux.output()

    def zero(self):
        """returns True if all the output is False"""
        # or_ all the output then invert, this or gate will be true if any of the output is true
        #unpack the list of out() and pass it to or_
        # then not_ the or_ output
        return not_( or_(*self.out()))   

    def negative(self):
        """returns True if the number is negative"""
        return self.out()[0]

    def overflow(self):
        """returns True if the number is overflowed when doing addition"""
        return self.add_sub_overflow

    def carry_out(self):
        """"returns True if the number is overflowed when doing subtraction (in2 > in1)"""
        return self.add_sub_borrow_out
    


# test alu 
import random

num1 = random.randint(0, 255)
num2 = random.randint(0, 255)

# convert the integers to lists of boolean values
input1 = [bool(int(bit)) for bit in f"{num1:08b}"]
input2 = [bool(int(bit)) for bit in f"{num2:08b}"]
# randomly generate control1
control1 = random.choice([True, False])
control2 = random.choice([True, False])

alu = ALU(input1, input2, control1, control2)

# if not control1 and not control2:
#     """Add"""
#     expected = num1 + num2
#     expected_overflow = False
#     if expected > 255:
#         expected = expected - 256 
#         expected_overflow = True
    
#     assert alu.out() == [bool(int(bit)) for bit in f"{expected:08b}"]
#     assert alu.overflow() == expected_overflow

