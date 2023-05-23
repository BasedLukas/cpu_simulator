class Registers:
    def __init__(self):
        self.registers = {
            'REGISTER_A': 0,
            'REGISTER_B': 0,
            'REGISTER_ARG': 0,
            'REGISTER_FLAGS': 0,
            'REGISTER_PC': 0,
            'REGISTER_IR': 0,
            'REGISTER_GENERAL1': 0,
            'REGISTER_GENERAL2': 0,
            'REGISTER_GENERAL3': 0,
            'REGISTER_GENERAL4': 0,
            'REGISTER_GENERAL5': 0,
            'REGISTER_GENERAL6': 0,
            'REGISTER_NULL': 0,
        }

    def __getitem__(self, key):
        return self.registers[key]

    def __setitem__(self, key, value):
        self.registers[key] = value
