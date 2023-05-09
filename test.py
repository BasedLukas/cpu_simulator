
import unittest
import gates
import basic_components
import random

class TestGates(unittest.TestCase):
    
    def test_logic_gates(self):
        """test that logic gate outputs work as intended"""
        input1 = True
        input2 = False

        assert gates.and_(input1, input2) == False
        assert gates.and_(input1, input1) == True


        assert gates.or_(input1, input2) == True
        assert gates.or_(input2, input2) == False
        assert gates.or_(input1, input1) == True


        assert gates.not_(input1) == False
        assert gates.not_(input2) == True
        

        assert gates.nand(input1, input2) == True
        assert gates.nand(input1, input1) == False
        assert gates.nand(input2, input2) == True

        
        assert gates.nor(input1, input2) == False
        assert gates.nor(input2, input2) == True

        assert gates.xor(input1, input2) == True
        assert gates.xor(input1, input1) == False

        assert gates.xnor(input1, input2) == False
        assert gates.xnor(input1, input1) == True  
    def test_gates_connected_in_series(self):
        """test that multiple gates can be connected in series"""
        input1 = True
        input2 = False

        and_gate = gates.and_(input1, input2)
        and_gate2 = gates.and_(input1, input1)
        or_gate = gates.or_(and_gate, and_gate2)
        not_gate = gates.not_(or_gate)
        assert or_gate == True
        assert not_gate == False



class TestBasicComponents(unittest.TestCase):

    def test_half_adder(self):
        """if both true then carry is true and sum is false
        if one true and one false then carry is false and sum is true
        if both false then carry is false and sum is false"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]

        for in1, in2 in zip(input1, input2):
            half_adder = basic_components.HalfAdder(in1, in2)
            if in1 and in2:
                assert half_adder.carry() == True
                assert half_adder.sum() == False
            elif in1 or in2:
                assert half_adder.carry() == False
                assert half_adder.sum() == True
            else:
                assert half_adder.carry() == False
                assert half_adder.sum() == False
    def test_full_adder(self):
        """if all three inputs are true then carry is true and sum is true
        if two inputs are true then carry is true and sum is false
        if one input is true then carry is false and sum is true
        if all inputs are false then carry is false and sum is false"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]
        carry_in = [random.choice([True, False]) for x in range(100)]

        for in1, in2, carry in zip(input1, input2, carry_in):
            full_adder = basic_components.FullAdder(in1, in2, carry)
            if in1 and in2 and carry:
                assert full_adder.carry() == True
                assert full_adder.sum() == True
            elif (in1 and in2) or (in1 and carry) or (in2 and carry):
                assert full_adder.carry() == True
                assert full_adder.sum() == False
            elif in1 or in2 or carry:
                assert full_adder.carry() == False
                assert full_adder.sum() == True
            else:
                assert full_adder.carry() == False
                assert full_adder.sum() == False
    def test_adder(self):
        """the adder takes in two 8 bit lists and an optional carry in and ads them"""
        #randomly generate to 8 bit lists
        input1 = [random.choice([True, False]) for x in range(8)]
        input2 = [random.choice([True, False]) for x in range(8)]

        #convert the lists to ints
        int1 = int("".join([str(int(x)) for x in input1]), 2)
        int2 = int("".join([str(int(x)) for x in input2]), 2)

        adder = basic_components.Adder(input1, input2)
        assert adder.sum() == 

if __name__ == '__main__':
    unittest.main()





