from src.cpu import CPU
from src.memory import Memory
from src.registers import Registers




def main():
    # Create instances of CPU, Memory, and Registers
    cpu = CPU()
    memory = Memory()
    registers = Registers()

    # Initialize registers with numbers
    registers['REGISTER_A'] = 10
    registers['REGISTER_B'] = 9

    # Initialize memory with instructions
    memory[0] = 'CPU_ADD'  # Add contents of A and B, result in A

    memory[1] = 'CPU_STA'  # Store A into memory

    memory[2] = 'CPU_LDA'  # Load A from memory

    memory[3] = 'CPU_PRT'  # Print A

    memory[4] = 'CPU_HLT'  # Halt





    # Start the CPU
    cpu.execute(memory, registers)

if __name__ == "__main__":
    main()


