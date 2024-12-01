
from assembler import Assembler


from src.hardware.cpu import CPU
from src.assembler.assembler import assemble_binary as ab


class Assembler(Assembler):
    def assemblebinary(self, program_string:str)-> str:
        binary = ab(code_string=program_string)
        return str(binary)
        