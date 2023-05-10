
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
    #TODO add test
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
        self.input2 = input2
        self.full_subtractors = []

        # Process the bits from right to left (LSB to MSB)
        for bit1, bit2 in zip(reversed(self.input1), reversed(self.input2)):
            full_subtractor = FullSubtractor(bit1, bit2, borrow_in)
            self.full_subtractors.append(full_subtractor)
            borrow_in = full_subtractor.borrow()

    def diff(self) -> list[bool]:
        # Reverse the sum result to get the correct order of bits (MSB to LSB)
        return list(reversed([full_subtractor.diff() for full_subtractor in self.full_subtractors]))

    def borrow_out(self) -> bool:
        return self.full_subtractors[-1].borrow()
