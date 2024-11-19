
from .gates import and_, or_, not_
from .basic_components import AddSub, Mux8Bit



class ALUResult:
    """Encapsulates the result of the ALU operation, providing access to the output and status flags."""

    def __init__(self, output, zero_func, negative_func, overflow_flag, carry_out_flag):
        self.out = output
        self._zero_func = zero_func
        self._negative_func = negative_func
        self._overflow_flag = overflow_flag
        self._carry_out_flag = carry_out_flag

    @property
    def zero(self):
        """bool: True if all bits in the output are False."""
        return self._zero_func()

    @property
    def negative(self):
        """bool: True if the output represents a negative number."""
        return self._negative_func()

    @property
    def overflow(self):
        """bool: True if there is an overflow when performing addition."""
        return self._overflow_flag

    @property
    def carry_out(self):
        """bool: True if there is a borrow out when performing subtraction (in2 > in1)."""
        return self._carry_out_flag


def alu(input1: list[bool], input2: list[bool], control1: bool, control2: bool):
    """
    Simulates an Arithmetic Logic Unit (ALU) with specified control signals.

    ALU operations based on control signals:
        control1 | control2
        0        | 0        = Add
        0        | 1        = Or
        1        | 0        = Subtract
        1        | 1        = And

    Args:
        input1 (list[bool]): First 8-bit input operand.
        input2 (list[bool]): Second 8-bit input operand.
        control1 (bool): First control signal.
        control2 (bool): Second control signal.

    Returns:
        ALUResult: An object with attributes and properties:
            - out (list[bool]): The output of the ALU.
            - zero (bool): True if all bits in the output are False.
            - negative (bool): True if the output represents a negative number.
            - overflow (bool): True if there is an overflow in addition.
            - carry_out (bool): True if there is a carry out in subtraction.

    Raises:
        ValueError: If either input1 or input2 is not 8 bits long.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Both inputs must be 8 bits long.")

    # Perform addition or subtraction based on control1
    add_sub = AddSub(input1, input2, control1)
    add_sub_out = add_sub.output()  # If control1 == True then subtract else add

    add_sub_overflow = add_sub.overflow()      # Used when doing addition
    add_sub_borrow_out = add_sub.borrow_out()  # Used when doing subtraction (in2 > in1)

    # Perform bitwise AND and OR operations
    and_out = [and_(in1, in2) for in1, in2 in zip(input1, input2)]
    or_out = [or_(in1, in2) for in1, in2 in zip(input1, input2)]

    # First Mux: selects between AND and OR outputs based on control1
    and_or_mux = Mux8Bit(and_out, or_out, control1)
    and_or_mux_out = and_or_mux.output()

    # Second Mux: selects between add/sub output and and/or output based on control2
    final_mux = Mux8Bit(and_or_mux_out, add_sub_out, control2)
    alu_output = final_mux.output()

    # Function to determine if all bits in output are zero
    def zero():
        """Returns True if all bits in the output are False."""
        # Use or_ to check if any bit is True, then invert
        return not or_(*alu_output)

    # Function to check if the output represents a negative number
    def negative():
        """Returns True if the output represents a negative number."""
        # In two's complement, the most significant bit indicates sign
        return alu_output[0]

    # Create ALUResult instance with output and status flags
    return ALUResult(
        output=alu_output,
        zero_func=zero,
        negative_func=negative,
        overflow_flag=add_sub_overflow,
        carry_out_flag=add_sub_borrow_out,
    )


# class ALU:
#     """"
# ALU rules;
#     control1 | control2
#     0        | 0        = Add
#     0        | 1        = Or
#     1        | 0        = Subtract
#     1        | 1        = And

#     input1 - input2 = output   
#     zero() = True if all the output is False
#     negative() = True if the number is negative
#     overflow() = True if the number is overflowed when doing addition
#     carry_out() = True if the number is overflowed when doing subtraction (in2 > in1) 
#         """
#     def __init__(self, input1: list[bool], input2: list[bool], control1:bool, control2:bool):
#         if len(input1) != 8 or len(input2) != 8:
#             raise ValueError("Both inputs must be 8 bits long.")
#         self.input1 = input1
#         self.input2 = input2
#         self.control1 = control1
#         self.control2 = control2
    
#         # create add sub
#         add_sub = AddSub(self.input1, self.input2, self.control1)
#         add_sub_out = add_sub.output() # if control1 == True then subtract else add
        
#         self.add_sub_overflow = add_sub.overflow() # used when doing addition
#         self.add_sub_borrow_out = add_sub.borrow_out() # used when doing subtraction (in2 > in1)


#         #create bitwise operations
#         and_out = [and_(in1, in2) for in1, in2 in zip(self.input1, self.input2)]
#         or_out = [or_(in1, in2) for in1, in2 in zip(self.input1, self.input2)]

#         #pass and or output to mux
#         and_or_mux = Mux8Bit(and_out, or_out, self.control1)
#         and_or_mux_out = and_or_mux.output()

#         #pass and or mux out + add sub out to mux
#         self.and_or_add_sub_mux = Mux8Bit(and_or_mux_out, add_sub_out, self.control2)


#     def out(self):
#         """returns the output of the ALU"""
#         return self.and_or_add_sub_mux.output()

#     def zero(self):
#         """returns True if all the output is False"""
#         # or_ all the output then invert, this or gate will be true if any of the output is true
#         #unpack the list of out() and pass it to or_
#         # then not_ the or_ output
#         return not_( or_(*self.out()))   

#     def negative(self):
#         """returns True if the number is negative"""
#         return self.out()[0]

#     def overflow(self):
#         """returns True if the number is overflowed when doing addition"""
#         return self.add_sub_overflow

#     def carry_out(self):
#         """"returns True if the number is overflowed when doing subtraction (in2 > in1)"""
#         return self.add_sub_borrow_out
    


