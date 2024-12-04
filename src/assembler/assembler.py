from typing import List, Optional

reserved_keywords =[
    "add",
    "or",
    "sub",
    "and",
    "eval",
    "copy",
    "label"
]
symbol_to_value = {
    'never': 0,
    '=': 1,
    '<': 2,
    '<=': 3,
    'always': 4,
    '!=': 5,
    '>=': 6,
    '>': 7
}
opp_to_value = {
    'add': [0, 1, 0, 0, 0, 0, 0, 0],
    'or':  [0, 1, 0, 0, 0, 0, 0, 1],
    'sub': [0, 1, 0, 0, 0, 0, 1, 0],
    'and': [0, 1, 0, 0, 0, 0, 1, 1]
}




def get_lines(filename: Optional[str] = None, code_string: Optional[str] = None) -> List[List[str]]:
    """
    Reads lines from a file or code string, removes comments and empty lines,
    and splits lines into instructions.

    Args:
        filename (str, optional): Path to the input file containing assembly code.
        code_string (str, optional): A string containing assembly code.

    Returns:
        List[List[str]]: A list of instructions, where each instruction is a list of strings.

    Raises:
        ValueError: If neither 'filename' nor 'code_string' is provided, or if both are provided.
    """
    if filename and code_string:
        raise ValueError("provide either a file path or a code string")
    elif filename:
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            raise ValueError("Couldn't read file")
    elif code_string:
        # Read from a code string
        if isinstance(code_string, str):
            lines = code_string.strip().splitlines()
        else:
            raise ValueError("unable to process code string")
    else:
        raise ValueError("provide a valid input to assemble")

    # Remove comments and empty lines
    lines = [
        line.split('#')[0].strip()
        for line in lines
        if line.strip() and not line.strip().startswith('#')
    ]
    # Split lines into instructions
    instructions = [line.split() for line in lines]
    return instructions




def assemble_binary(filename: Optional[str] = None, code_string: Optional[str] = None) -> List[List[int]]:
    """
    Processes lines containing binary instructions from a file or a code string.
    Skips lines with comments or empty lines.

    Args:
        filename (str, optional): Path to the input file containing assembly code.
        code_string (str, optional): A string containing assembly code.

    Returns:
        List[List[int]]: A list where each inner list represents processed binary instructions.

    Raises:
        ValueError: If neither 'filename' nor 'code_string' is provided, or if both are provided.
    """
    lines = get_lines(filename, code_string)
    labels = {}
    program = []

    pc = 0
    for i, instruction in enumerate(lines, start=1):
        if instruction[0] == 'label':
            if pc > 63:
                raise ValueError(f"overflow error, labels cannot be placed past instruction 63 (currently {pc}), near line {i}:{instruction}")
            if labels.get(instruction[1],None) is not None:
                raise ValueError(f"label cannot be declared twice, near line {i}: {instruction}")
            if len(instruction) != 2:
                raise ValueError(f"Expected label followed by name, near line {i}:{instruction}")
            label = instruction[1]
            if label in reserved_keywords or label.isdigit():
                raise ValueError(f"Cannot use {label} as a label name, near line {i}:{instruction}")
            labels[instruction[1]] = pc
        else:
            pc += 1

    for i, instruction in enumerate(lines, start=1):
        match instruction[0]:
            case 'label':
                continue

            case _ if instruction[0].isdigit():
                value = int(instruction[0])
                valid_immediate = range(0,64)
                if  value not in valid_immediate:
                    raise ValueError(f"immediate values cannot be larger than 63, near line {i}:{instruction}")
                if len(instruction) != 1:
                    raise ValueError(f"Immediate value takes no args, near line {i}:{instruction}")
                value = [int(bit) for bit in format(value, '08b')]
                program.append(value)

            case 'copy':
                if len(instruction) != 3:
                    raise ValueError(f"incorrect copy instruction, near line {i}: {instruction}")
                source = int(instruction[1])
                destination = int(instruction[2])
                valid_range = range(0,7)
                if source not in valid_range or destination not in valid_range:
                    raise ValueError(f"copy src dest, must be between 0-6 near line {i}: {instruction}")
                copy_instruction = [1, 0]
                src = [int(bit) for bit in format(source, '03b')]
                dst = [int(bit) for bit in format(destination, '03b')]
                value = copy_instruction + src + dst
                program.append(value)

            case 'add' | 'or'| 'and' | 'sub':
                if len(instruction) != 1:
                    raise ValueError(f"Operation instructions take no args, near lin {i}:{instruction}")
                value = opp_to_value[instruction[0]]
                program.append(value)

            case 'eval':
                if len(instruction) != 2:
                    raise ValueError(f"eval must be followed by 1 operator, near line {i}:{instruction}")
                value = symbol_to_value.get(instruction[1], None)
                if value is None:
                    raise ValueError(f"evaluations can only use one of {symbol_to_value.keys()}, near line {i}:{instruction}")
                value = [1, 1, 0, 0, 0] + [int(bit) for bit in format(value, '03b')]
                program.append(value)

            case _ :
                value = labels.get(instruction[0], None)
                if value is not None:
                    value = [int(bit) for bit in format(value, '08b')]
                    program.append(value)
                else:
                    # we encountered a bad instruction
                    raise ValueError(
                        f"Invalid instruction near line {i}:{instruction}"
                    )


    return program
     
