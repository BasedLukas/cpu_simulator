


def assemble_instruction(instruction):
    parts = instruction.split()
    opcode = parts[0].lower()

    if opcode.isdigit():
        # Immediate instruction
        value = int(opcode)
        if value < 0 or value > 63:
            raise ValueError(f'Invalid immediate value: {value}')
        return [0, 0] + [int(bit) for bit in format(value, '06b')]
    elif opcode == 'add':
        # Operate instruction (add)
        return [0, 1, 0, 0, 0, 0, 0, 0]
    elif opcode == 'or':
        # Operate instruction (or)
        return [0, 1, 0, 0, 0, 0, 0, 1]
    elif opcode == 'subtract':
        # Operate instruction (subtract)
        return [0, 1, 0, 0, 0, 0, 1, 0]
    elif opcode == 'and':
        # Operate instruction (and)
        return [0, 1, 0, 0, 0, 0, 1, 1]
    elif opcode == 'copy':
        # Copy instruction
        src, dst = map(int, parts[1:])
        return [1, 0] + [int(bit) for bit in format(src, '03b')] + [int(bit) for bit in format(dst, '03b')]
    elif opcode == 'eval':
        # Eval instruction
        relevant_bits = parts[1]
        return [1, 1, 0, 0, 0] + [int(bit) for bit in relevant_bits]
        
    else:
        raise ValueError(f'Unknown opcode: {opcode}')

def assemble_binary(filename):
    program = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore empty lines and comments
                instruction = assemble_instruction(line)
                program.append(instruction)
                
    return program


