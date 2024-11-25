


from .gates import and_, or_, not_, nand, nor, xor, xnor
from types import SimpleNamespace as sn


def half_adder(input1:bool, input2:bool):
    return sn(
        sum=xor(input1, input2),
        carry=and_(input1, input2)
        )

    

def full_adder(input1:bool, input2:bool, carry_in:bool):
    half_adder1 = half_adder(input1, input2)
    half_adder2 = half_adder(half_adder1.sum, carry_in)
    out = sn(
        sum=half_adder2.sum,
        carry=or_(half_adder1.carry, half_adder2.carry)
    )
    return out


def adder(input1: list[bool], input2: list[bool], carry_in: bool = False):
    """
    Simulates an 8-bit adder using a list of full adders.

    Args:
        input1 (list[bool]): First 8-bit binary number as a list of booleans.
        input2 (list[bool]): Second 8-bit binary number as a list of booleans.
        carry_in (bool): Initial carry-in bit.

    Returns:
        SimpleNamespace: An object with `.sum` and `.carry_out` properties.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Both inputs must be 8 bits long.")

    full_adders = []
    carry = carry_in

    # Process bits from right to left (LSB to MSB)
    for bit1, bit2 in zip(reversed(input1), reversed(input2)):
        out = full_adder(bit1, bit2, carry)
        full_adders.append(out)
        carry = out.carry

    # Extract the sum (in reverse order to maintain LSB to MSB processing)
    sum_result = list(reversed([f.sum for f in full_adders]))

    # Return a namespace mimicking the original behavior
    return sn(
        sum=sum_result,
        carry_out=carry
    )

    
def half_subtractor(input1: bool, input2: bool):
    """
    Simulates a half subtractor circuit.

    Args:
        input1 (bool): The minuend (input1 - input2).
        input2 (bool): The subtrahend.

    Returns:
        SimpleNamespace: An object with `.diff` and `.borrow` properties.
    """
    diff = xor(input1, input2)
    borrow = and_(not_(input1), input2)
    return sn(
        diff=diff,
        borrow=borrow
    )


def full_subtractor(input1: bool, input2: bool, borrow_in: bool):
    """
    Simulates a full subtractor circuit.

    Args:
        input1 (bool): The minuend (input1 - input2 - borrow_in).
        input2 (bool): The subtrahend.
        borrow_in (bool): Borrow input from the previous bit.

    Returns:
        SimpleNamespace: An object with `.diff` and `.borrow` properties.
    """
    half_subtractor1 = half_subtractor(input1, input2)
    half_subtractor2 = half_subtractor(half_subtractor1.diff, borrow_in)

    diff = half_subtractor2.diff
    borrow = or_(half_subtractor1.borrow, half_subtractor2.borrow)

    return sn(
        diff=diff,
        borrow=borrow
    )

    
def subtractor(input1: list[bool], input2: list[bool], borrow_in: bool = False):
    """
    Simulates an 8-bit subtractor using an adder.

    Args:
        input1 (list[bool]): First 8-bit binary number (minuend).
        input2 (list[bool]): Second 8-bit binary number (subtrahend).
        borrow_in (bool): Initial borrow-in bit.

    Returns:
        SimpleNamespace: An object with `.diff` and `.borrow_out` properties.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Both inputs must be 8 bits long.")

    # Invert input2 and borrow_in for subtraction
    inverted_input2 = [not_(x) for x in input2]
    carry_in = not_(borrow_in)

    # Use adder for subtraction
    result = adder(input1, inverted_input2, carry_in)

    return sn(
        diff=result.sum,
        borrow_out=not_(result.carry_out)  # borrow_out is the inverse of carry_out
    )


def mux(input1: bool, input2: bool, sel: bool) -> bool:
    """
    Simulates a 2-to-1 multiplexer using NAND gates.

    Args:
        input1 (bool): Input 1.
        input2 (bool): Input 2.
        sel (bool): Select signal (True for input2, False for input1).

    Returns:
        bool: Output of the multiplexer.
    """
    nand_central = nand(sel, sel)
    nand1 = nand(input1, sel)
    nand2 = nand(input2, nand_central)
    output = nand(nand1, nand2)
    return output


def mux_8bit(input1: list[bool], input2: list[bool], sel: bool) -> list[bool]:
    """
    Simulates an 8-bit 2-to-1 multiplexer.

    Args:
        input1 (list[bool]): First 8-bit binary number.
        input2 (list[bool]): Second 8-bit binary number.
        sel (bool): Select signal (True for input2, False for input1).

    Returns:
        list[bool]: Output of the 8-bit multiplexer.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Inputs should be 8 bits.")
    
    return [mux(bit1, bit2, sel) for bit1, bit2 in zip(input1, input2)]


def mux_8bit(input1: list[bool], input2: list[bool], sel: bool) -> list[bool]:
    """
    Simulates an 8-bit 2-to-1 multiplexer.

    Args:
        input1 (list[bool]): First 8-bit binary number.
        input2 (list[bool]): Second 8-bit binary number.
        sel (bool): Select signal (True for input2, False for input1).

    Returns:
        list[bool]: Output of the 8-bit multiplexer.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Inputs should be 8 bits.")
    
    return [mux(bit1, bit2, sel) for bit1, bit2 in zip(input1, input2)]


def add_sub(input1: list[bool], input2: list[bool], operation: bool):
    """
    Simulates an 8-bit add/subtract unit.

    Args:
        input1 (list[bool]): First 8-bit binary number.
        input2 (list[bool]): Second 8-bit binary number.
        operation (bool): True for subtraction, False for addition.

    Returns:
        SimpleNamespace: An object with `.output`, `.overflow`, and `.borrow_out` properties.
    """
    if len(input1) != 8 or len(input2) != 8:
        raise ValueError("Both inputs must be 8 bits long.")

    # XOR input2 with operation to conditionally invert input2
    adjusted_input2 = [xor(x, operation) for x in input2]

    # Use adder for addition or subtraction
    result = adder(input1, adjusted_input2, operation)

    return sn(
        output=result.sum,
        overflow=result.carry_out,      # Carry-out used for addition overflow
        borrow_out=not_(result.carry_out)  # Inverse carry-out used for subtraction borrow-out
    )


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

