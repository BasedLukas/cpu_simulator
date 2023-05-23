class Memory:
    def __init__(self):
        self.memory = [0] * 256

    def __getitem__(self, address):
        return self.memory[address]

    def __setitem__(self, address, value):
        self.memory[address] = value
