from typing import List


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
    'or': [0, 1, 0, 0, 0, 0, 0, 1],
    'sub': [0, 1, 0, 0, 0, 0, 1, 0],
    'and': [0, 1, 0, 0, 0, 0, 1, 1]
}


def assemble_binary(filename: str) -> List[List[int]]:
    """
    Reads a file and processes lines containing binary instructions.
    Skips lines with comments or empty lines.

    :param filename: Path to the input file.
    :return: A list of lists, where each inner list represents processed binary instructions.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    lines = [line.split('#')[0].strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    lines = [line.split() for line in lines]

    labels = {}
    program = []

    pc = 0
    for i, instruction in enumerate(lines, start=1):
        if instruction[0] == 'label':
            if pc > 63:
                raise ValueError(f"overflow error, labels cannot be placed past instruction 63 (currently {pc}), near line {i}:{instruction}")
            if labels.get(instruction[1],None) is not None:
                raise ValueError(f"label cannot be declared twice, near line {i}: {instruction}")
            labels[instruction[1]] = pc
        else:
            pc += 1

    for i, instruction in enumerate(lines, start=1):
        match instruction[0]:
            case 'label':
                continue

            case _ if instruction[0].isdigit():
                value = int(instruction[0])
                if  0 > value > 63:
                    raise ValueError(f"immediate values cannot be larger than 63, near line {i}:{instruction}")
                value = [int(bit) for bit in format(value, '08b')]
                program.append(value)

            case 'copy':
                if len(instruction) != 3:
                    raise ValueError(f"incorrect copy instruction, near line {i}: {instruction}")
                source = int(instruction[1])
                destination = int(instruction[2])
                if 0 > source > 6 or 0 > destination > 6:
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
     
