def cpu_nop(registers, memory, running):
    pass

def cpu_lda(registers, memory, running):
    registers['REGISTER_A'] = memory[registers['REGISTER_ARG']]

def cpu_ldb(registers, memory, running):
    registers['REGISTER_B'] = memory[registers['REGISTER_ARG']]

def cpu_ldg(registers, memory, running):
    registers['REGISTER_GENERAL1'] = memory[registers['REGISTER_ARG']]

def cpu_sta(registers, memory, running):
    memory[registers['REGISTER_ARG']] = registers['REGISTER_A']

def cpu_stg(registers, memory, running):
    memory[registers['REGISTER_ARG']] = registers['REGISTER_GENERAL1']

def cpu_emt(registers, memory, running):
    print(chr(memory[registers['REGISTER_ARG']]), end='')

def cpu_prt(registers, memory, running):
    print()
    print(memory[registers['REGISTER_ARG']], end='')
    print()

def cpu_lsh(registers, memory, running):
    registers['REGISTER_A'] <<= registers['REGISTER_ARG']

def cpu_rsh(registers, memory, running):
    registers['REGISTER_A'] >>= registers['REGISTER_ARG']

def cpu_inc(registers, memory, running):
    registers['REGISTER_A'] += registers['REGISTER_ARG']

def cpu_dec(registers, memory, running):
    registers['REGISTER_A'] -= registers['REGISTER_ARG']

def cpu_cla(registers, memory, running):
    registers['REGISTER_A'] = 0

def cpu_clb(registers, memory, running):
    registers['REGISTER_B'] = 0

def cpu_clg(registers, memory, running):
    registers['REGISTER_GENERAL1'] = 0

def cpu_clf(registers, memory, running):
    registers['REGISTER_FLAGS'] = 0

def cpu_add(registers, memory, running):
    registers['REGISTER_A'] += registers['REGISTER_B']

def cpu_sub(registers, memory, running):
    registers['REGISTER_A'] -= registers['REGISTER_B']

def cpu_mul(registers, memory, running):
    registers['REGISTER_A'] *= registers['REGISTER_B']

def cpu_div(registers, memory, running):
    registers['REGISTER_A'] //= registers['REGISTER_B']

def cpu_neg(registers, memory, running):
    registers['REGISTER_A'] = -registers['REGISTER_A']

def cpu_and(registers, memory, running):
    registers['REGISTER_A'] &= registers['REGISTER_B']

def cpu_or(registers, memory, running):
    registers['REGISTER_A'] |= registers['REGISTER_B']

def cpu_not(registers, memory, running):
    registers['REGISTER_A'] = ~registers['REGISTER_A']

def cpu_cmp(registers, memory, running):
    registers['REGISTER_FLAGS'] = registers['REGISTER_A'] == registers['REGISTER_B']

def cpu_nul(registers, memory, running):
    memory[registers['REGISTER_ARG']] = 0

def cpu_jmp(registers, memory, running):
    registers['REGISTER_PC'] = registers['REGISTER_ARG']

def cpu_jmr(registers, memory, running):
    registers['REGISTER_PC'] += registers['REGISTER_ARG']

def cpu_jin(registers, memory, running):
    if not registers['REGISTER_FLAGS']:
        registers['REGISTER_PC'] = registers['REGISTER_ARG']

def cpu_jie(registers, memory, running):
    if registers['REGISTER_FLAGS']:
        registers['REGISTER_PC'] = registers['REGISTER_ARG']

def cpu_hlt(registers, memory, running):
    running[0] = False
