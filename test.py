
import unittest
import gates
from gates import and_, or_, not_, nand, nor, xor, xnor
from basic_components import HalfAdder, FullAdder, Adder, HalfSubtractor, FullSubtractor, Subtractor, Mux
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

        for i in range(1000):
            test_adder_once()

    def test_half_subtractor(self):
        """Test various cases for HalfSubtractor"""

        input1 = [random.choice([True, False]) for x in range(100)]
        input2 = [random.choice([True, False]) for x in range(100)]

        for in1, in2 in zip(input1, input2):
            half_subtractor = HalfSubtractor(in1, in2)
            if in1 and in2:
                assert half_subtractor.borrow() == False
                assert half_subtractor.diff() == False
            elif in1 and not in2:
                assert half_subtractor.borrow() == False
                assert half_subtractor.diff() == True
            elif in2 and not in1:
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
            if not in1 and not in2 and not borrow:
                assert full_subtractor.borrow() == False
                assert full_subtractor.diff() == False
            elif in1 and not in2 and not borrow:
                assert full_subtractor.borrow() == False
                assert full_subtractor.diff() == True
            elif in2 and not in1 and not borrow:
                assert full_subtractor.borrow() == True
                assert full_subtractor.diff() == True
            elif in1 and in2 and not borrow:
                assert full_subtractor.borrow() == False
                assert full_subtractor.diff() == False
            elif not in1 and not in2 and borrow:
                assert full_subtractor.borrow() == True
                assert full_subtractor.diff() == True
            elif in1 and not in2 and borrow:
                assert full_subtractor.borrow() == False
                assert full_subtractor.diff() == False
            elif in2 and not in1 and borrow:
                assert full_subtractor.borrow() == True
                assert full_subtractor.diff() == False
            elif in1 and in2 and borrow:
                assert full_subtractor.borrow() == True
                assert full_subtractor.diff() == True

    def test_subtractor(self):
        """test the subtractor class multiple times with random values"""
        
        def test_subtractor_once():
            """the subtractor takes in two 8-bit lists and an optional borrow in and subtracts them"""
            # randomly generate two 8-bit integers
            num1 = random.randint(0, 255)
            num2 = random.randint(0, 255)
            result = num1 - num2

            # randomly generate a borrow-in value
            borrow_in = random.choice([True, False])

            # convert the integers to lists of boolean values
            input1 = [bool(int(bit)) for bit in f"{num1:08b}"]
            input2 = [bool(int(bit)) for bit in f"{num2:08b}"]

            # use the Subtractor class to compute the difference with borrow-in
            subtractor = Subtractor(input1, input2, borrow_in)
            diff_result = subtractor.diff()
            borrow_out = subtractor.borrow_out()

            # convert the diff result back to an integer
            diff_result_int = int("".join([str(int(x)) for x in diff_result]), 2)

            # expected borrow-out value
            expected_borrow_out = (num1 - int(borrow_in)) < num2


            # if num1 > num2, then diff_result should equal result - borrow_in
            if num1 >= num2:
                expected_diff = result - int(borrow_in)
                expected_diff %= 256  # apply modulo 256 for wrap around
            # if num1 < num2, then diff_result should equal result + 256 - borrow_in
            else:
                expected_diff = result + 256 - int(borrow_in)

            # compare the diff result with the expected diff
            self.assertEqual(diff_result_int, expected_diff, f"Expected {expected_diff}, got {diff_result_int}")

            # compare the borrow-out value with the expected borrow-out value
            self.assertEqual(borrow_out, expected_borrow_out, f"Expected borrow_out {expected_borrow_out}, got {borrow_out}")

        for i in range(1000):
            test_subtractor_once()
          


    def test_mux(self):
        select = False
        assert Mux(False, False, select).output() == False
        assert Mux(False, True, select).output() == True
        assert Mux(True, False, select).output() == False
        assert Mux(True, True, select).output() == True
        select = True
        assert Mux(False, False, select).output() == False
        assert Mux(True, False, select).output() == True
        assert Mux(False, True, select).output() == False
        assert Mux(True, True, select).output() == True


if __name__ == '__main__':
    unittest.main()





