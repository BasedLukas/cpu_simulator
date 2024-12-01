
from cpuworld import Cpuworld
from src.hardware.cpu import CPU

class Cpuworld(Cpuworld):

    def __init__(self):
        self.cpu = None

    def cpuinit(self, program):
        print(f"type input:{type(program)}")
        program = eval(program)
        cpu = CPU(program)
        cpu.run()
        return str(cpu.reg.output)

        