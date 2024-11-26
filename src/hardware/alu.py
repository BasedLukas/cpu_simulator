from .gates import and_, or_, not_
from .basic_components import add_sub, mux_8bit
from types import SimpleNamespace


def alu(input1: list[bool], input2: list[bool], control1: bool, control2: bool):
    """
    Simulates an 8-bit Arithmetic Logic Unit (ALU) with specified control signals.

    The ALU performs one of four operations based on the control signals:
        - If control1 == False and control2 == False: Add input1 and input2.
        - If control1 == False and control2 == True:  Bitwise OR of input1 and input2.
        - If control1 == True  and control2 == False: Subtract input2 from input1.
        - If control1 == True  and control2 == True:  Bitwise AND of input1 and input2.

    Args:
        input1 (list[bool]): First 8-bit input operand (most significant bit first).
        input2 (list[bool]): Second 8-bit input operand (most significant bit first).
        control1 (bool): First control signal.
        control2 (bool): Second control signal.

    Returns:
        SimpleNamespace: An object with the following attributes:
            - out (list[bool]): The 8-bit output of the ALU.
            - zero (bool): True if all bits in the output are False.
            - negative (bool): True if the output represents a negative number (MSB is True).
            - overflow (bool): True if there is an overflow in addition or subtraction.
            - carry_out (bool): True if there is a carry out in addition or borrow out in subtraction.

    Raises:
        ValueError: If either input1 or input2 is not 8 bits long.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Both inputs must be 8 bits long.")

    # Perform addition or subtraction based on control1
    add_sub_result = add_sub(input1, input2, control1)
    add_sub_output = add_sub_result.output
    overflow_flag = add_sub_result.overflow  # Overflow in addition
    carry_out_flag = add_sub_result.borrow_out  # Borrow out in subtraction

    # Perform bitwise AND and OR operations
    and_output = [and_(in1, in2) for in1, in2 in zip(input1, input2)]
    or_output = [or_(in1, in2) for in1, in2 in zip(input1, input2)]

    # First multiplexer: selects between AND and OR outputs based on control1
    and_or_mux_output = mux_8bit(and_output, or_output, control1)

    # Second multiplexer: selects between add/sub output and and/or output based on control2
    final_output = mux_8bit(and_or_mux_output, add_sub_output, control2)

    # Determine zero flag (True if all bits are False)
    zero_flag = not or_(*final_output)

    # Determine negative flag (True if the most significant bit is True)
    negative_flag = final_output[0]

    # Return the result as a SimpleNamespace
    return SimpleNamespace(
        out=final_output,
        zero=zero_flag,
        negative=negative_flag,
        overflow=overflow_flag,
        carry_out=carry_out_flag,
    )
