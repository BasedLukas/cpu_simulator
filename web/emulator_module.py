
# wit
from emulator import Emulator

# python
from src.hardware.cpu import CPU
from src.assembler.assembler import assemble_binary as ab

class Emulator(Emulator):

    # def __init__(self):
    #     self.cpu = None

    def cpuinit(self, program):
        print(f"type input:{type(program)}")
        program = eval(program)
        cpu = CPU(program)
        cpu.run()
        return str(cpu.reg.output)

    def assemblebinary(self, program_string: str) -> str:
        binary = ab(code_string=program_string)
        return str(binary)