
import unittest
import gates
from gates import and_, or_, not_, nand, nor, xor, xnor
from basic_components import HalfAdder, FullAdder, Adder, HalfSubtractor, FullSubtractor, Subtractor
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
            half_adder = HalfAdder(in1, in2)
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
            full_adder = FullAdder(in1, in2, carry)
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
        """test the adder class multiple times with random values"""
        
        def test_adder_once():
            """the adder takes in two 8-bit lists and an optional carry in and adds them"""
            # randomly generate two 8-bit integers
            int1 = random.randint(0, 255)
            int2 = random.randint(0, 255)

            # randomly generate a carry-in value
            carry_in = random.choice([True, False])

            # convert the integers to lists of boolean values
            input1 = [bool(int(bit)) for bit in f"{int1:08b}"]
            input2 = [bool(int(bit)) for bit in f"{int2:08b}"]

            # use the Adder class to compute the sum with carry-in
            adder = Adder(input1, input2, carry_in)
            sum_result = adder.sum()
            carry_out = adder.carry_out()

            # compute the expected sum, account for carry-in
            expected_sum = int1 + int2 + int(carry_in)

            # expected carry-out value
            expected_carry_out = expected_sum > 255

            # apply modulo 256 for wrap around
            expected_sum %= 256

            # convert the sum result back to an integer
            sum_result_int = int("".join([str(int(x)) for x in sum_result]), 2)

            # compare the sum result with the expected sum
            assert sum_result_int == expected_sum, f"Expected {expected_sum}, got {sum_result_int}"

            # compare the carry-out value with the expected carry-out value
            assert carry_out == expected_carry_out, f"Expected carry_out {expected_carry_out}, got {carry_out}"

        for i in range(100):
            test_adder_once()

    def test_half_subtractor(self):
        """Test various cases for HalfSubtractor"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]

        for in1, in2 in zip(input1, input2):
            half_subtractor = HalfSubtractor(in1, in2)
            expected_diff = xor(in1, in2)
            expected_borrow = and_(not_(in1), in2)

            self.assertEqual(half_subtractor.diff(), expected_diff)
            self.assertEqual(half_subtractor.borrow(), expected_borrow)

    def test_full_subtractor(self):
        """Test various cases for FullSubtractor"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]
        borrow_in = [random.choice([True, False]) for x in range(100)]

        for in1, in2, borrow in zip(input1, input2, borrow_in):
            full_subtractor = FullSubtractor(in1, in2, borrow)

            # Calculate expected diff and borrow
            half_subtractor1 = HalfSubtractor(in1, in2)
            half_subtractor2 = HalfSubtractor(half_subtractor1.diff(), borrow)

            expected_diff = half_subtractor2.diff()
            expected_borrow = or_(half_subtractor1.borrow(), half_subtractor2.borrow())

            self.assertEqual(full_subtractor.diff(), expected_diff)
            self.assertEqual(full_subtractor.borrow(), expected_borrow)


    def test_half_subtractor(self):
        """Test various cases for HalfSubtractor"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]

        for in1, in2 in zip(input1, input2):
            half_subtractor = HalfSubtractor(in1, in2)
            if in1 and not in2:
                assert half_subtractor.borrow() == False
                assert half_subtractor.diff() == True
            elif not in1 and in2:
                assert half_subtractor.borrow() == True
                assert half_subtractor.diff() == True
            else:
                assert half_subtractor.borrow() == False
                assert half_subtractor.diff() == False

    def test_full_subtractor(self):
        """Test various cases for FullSubtractor"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]
        borrow_in = [random.choice([True, False]) for x in range(100)]

        for in1, in2, borrow in zip(input1, input2, borrow_in):
            full_subtractor = FullSubtractor(in1, in2, borrow)
            if in1 and not in2 and not borrow:
                assert full_subtractor.borrow() == False, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == True, f"Inputs: {in1}, {in2}, {borrow}"
            elif not in1 and in2 and not borrow:
                assert full_subtractor.borrow() == True, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == True, f"Inputs: {in1}, {in2}, {borrow}"
            elif not in1 and not in2 and borrow:
                assert full_subtractor.borrow() == True, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == True, f"Inputs: {in1}, {in2}, {borrow}"
            elif in1 and in2 and borrow:
                assert full_subtractor.borrow() == True, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == True, f"Inputs: {in1}, {in2}, {borrow}"
            elif (in1 and in2) or (in1 and borrow) or (in2 and borrow):
                assert full_subtractor.borrow() == True, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == False, f"Inputs: {in1}, {in2}, {borrow}"
            elif in1 or in2 or borrow:
                assert full_subtractor.borrow() == False, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == True, f"Inputs: {in1}, {in2}, {borrow}"
            else:
                assert full_subtractor.borrow() == False, f"Inputs: {in1}, {in2}, {borrow}"
                assert full_subtractor.diff() == False, f"Inputs: {in1}, {in2}, {borrow}"


if __name__ == '__main__':
    unittest.main()





