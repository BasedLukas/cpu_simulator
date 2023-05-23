from .instructions import *
from .memory import Memory
from .registers import Registers

class CPU:
    def __init__(self):
        self.memory = Memory()
        self.registers = Registers()
        self.running = [True]
        self.instructions = {
            'CPU_NOP': cpu_nop,
            'CPU_LDA': cpu_lda,
            'CPU_LDB': cpu_ldb,
            'CPU_LDG': cpu_ldg,
            'CPU_STA': cpu_sta,
            'CPU_STG': cpu_stg,
            'CPU_EMT': cpu_emt,
            'CPU_PRT': cpu_prt,
            'CPU_ADD': cpu_add,
            'CPU_SUB': cpu_sub,
            'CPU_MUL': cpu_mul,
            'CPU_DIV': cpu_div,
            'CPU_NEG': cpu_neg,
            'CPU_LSH': cpu_lsh,
            'CPU_RSH': cpu_rsh,
            'CPU_INC': cpu_inc,
            'CPU_DEC': cpu_dec,
            'CPU_CLA': cpu_cla,
            'CPU_CLB': cpu_clb,
            'CPU_CLG': cpu_clg,
            'CPU_CLF': cpu_clf,
            'CPU_CMP': cpu_cmp,
            'CPU_AND': cpu_and,
            'CPU_OR': cpu_or,
            'CPU_NOT': cpu_not,
            'CPU_NUL': cpu_nul,
            'CPU_JMP': cpu_jmp,
            'CPU_JMR': cpu_jmr,
            'CPU_JIN': cpu_jin,
            'CPU_JIE': cpu_jie,
            'CPU_HLT': cpu_hlt,
        }
        

    def execute(self, memory, registers):
        running = [True]
        while running[0]:
            pc = registers['REGISTER_PC']
            #print('PC now: ', pc)
            # Fetch
            ir = memory[pc]
            #print('IR now: ', ir)
            # Decode
            instruction = self.instructions[ir]
            #print('Instruction now: ', instruction)
            # Execute
            instruction(registers, memory, running)
            #print('Registers now: ', registers)
            #print('Memory now: ', memory)
            #print('Running now: ', running)
            # Increment PC
            registers['REGISTER_PC'] += 1



