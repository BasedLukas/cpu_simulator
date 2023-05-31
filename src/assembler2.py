

def convert_to_bits(integer):
    """takes in an integer and returns a byte"""
    return [int(bit) for bit in format(integer, '08b')]

def assemble_instruction(instruction):
    parts = instruction.split()
    part1 = parts[0].lower()



    if part1.isdigit():
        # Immediate instruction
        value = int(part1)
        if value < 0 or value > 63:
            raise ValueError(f'Invalid immediate value: {value}')
        return convert_to_bits(value)
    elif part1 == 'add':
        # Operate instruction (add)
        return [0, 1, 0, 0, 0, 0, 0, 0]
    elif part1 == 'or':
        # Operate instruction (or)
        return [0, 1, 0, 0, 0, 0, 0, 1]
    elif part1 == 'sub':
        # Operate instruction (subtract)
        return [0, 1, 0, 0, 0, 0, 1, 0]
    elif part1 == 'and':
        # Operate instruction (and)
        return [0, 1, 0, 0, 0, 0, 1, 1]
    elif part1 == 'copy':
        # Copy instruction = 10 
        cp = [1, 0]
        part2 = parts[1].lower()
        part3 = parts[2].lower()
        src = [int(bit) for bit in format(int(part2), '03b')]
        dst = [int(bit) for bit in format(int(part3), '03b')]
        return cp + src + dst
    
    elif part1 == 'eval':
        # Eval instruction
        part2 = parts[1].lower()

        if part2 == 'never':
            value = 0
        elif part2 == '=':
            value = 1
        elif part2 == '<':
            value = 2
        elif part2 == '<=':
            value = 3
        elif part2 == 'always':
            value = 4
        elif part2 == '!=':
            value = 5
        elif part2 == '>=':
            value = 6
        elif part2 == '>':
            value = 7
        else:
            raise ValueError(f'Unknown opcode: {part2}')
        return [1, 1, 0, 0, 0] + [int(bit) for bit in format(value, '03b')]

        
    else:
        print(instruction)
        raise ValueError(f'Unknown opcode')
        






def assemble_binary(filename):
    """takes in a file in cwd and returns binary program"""
    program = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore empty lines and comments
                line = line.split('#')[0]
                instruction = assemble_instruction(line)
                program.append(instruction)
                
    return program


