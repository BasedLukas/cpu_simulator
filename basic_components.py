
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


        for bit1, bit2 in zip(self.input1, self.input2):
            full_adder = FullAdder(bit1, bit2, carry_in)
            self.full_adders.append(full_adder)
            carry_in = full_adder.carry()

    def sum(self) -> list[bool]:
        return [full_adder.sum() for full_adder in self.full_adders]

    def carry_out(self) -> bool:
        return self.full_adders[-1].carry()
