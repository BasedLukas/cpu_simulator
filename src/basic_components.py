
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


class Decoder:
    """3 bit decoder, uses the 3 MSB in the input
    output is a list of 8 bits where 0 is MSB and 7 is LSB"""

    def __init__ (self, input:list[bool]):
        self.input = input[:3]
        self.output_list = [None]*8
        self.output_list[0] = and_(not_(self.input[0]), not_(self.input[1]), not_(self.input[2]))
        self.output_list[1] = and_(not_(self.input[0]), not_(self.input[1]), self.input[2])
        self.output_list[2] = and_(not_(self.input[0]), self.input[1], not_(self.input[2]))
        self.output_list[3] = and_(not_(self.input[0]), self.input[1], self.input[2])
        self.output_list[4] = and_(self.input[0], not_(self.input[1]), not_(self.input[2]))
        self.output_list[5] = and_(self.input[0], not_(self.input[1]), self.input[2])
        self.output_list[6] = and_(self.input[0], self.input[1], not_(self.input[2]))
        self.output_list[7] = and_(self.input[0], self.input[1], self.input[2])
    
    def output(self) -> list[bool]:
        return self.output_list

