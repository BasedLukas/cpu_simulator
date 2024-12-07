import pytest

from assembler.assembler import assemble_binary
from hardware.cpu import CPU

def to_int(byte):
    return int(''.join(map(str, byte)), 2)

def test_noop():
    cpu = CPU([[0,0,0,0,0,0,0,0]])
    cpu.run()


def test_immediate():
    code = """
    0
    1
    4
    63
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    for i in [0, 1, 4, 63]:
        cpu.exec()
        assert to_int(cpu.reg.registers[0]) == i

def test_copy():
    code = """
    17
    copy 0 3
    copy 3 4
    copy 4 5
    copy 5 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    for i in [0, 3, 4, 5]:
        cpu.exec()
        assert to_int(cpu.reg.registers[i]) == 17
    cpu.exec()
    assert to_int(cpu.reg.output) == 17

def test_math():
    code = """
    6
    copy 0 2
    5
    copy 0 1
    add
    copy 3 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert to_int(cpu.reg.output) == 11, "addition failed"
    
    code = """
    15
    copy 0 1
    5
    copy 0 2
    sub
    copy 3 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert to_int(cpu.reg.output) == 10, "subtraction failed"

    code = """
    5
    copy 0 1
    1
    copy 0 2
    and
    copy 3 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert to_int(cpu.reg.output) == 1,"AND failed"

    code = """
    4
    copy 0 1
    2
    copy 0 2
    or
    copy 3 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert to_int(cpu.reg.output) == 6,"OR failed"
    
def test_overflow_math():
    code = """
    32
    copy 0 1
    32
    copy 0 2
    add  # 64 in reg 3
    copy 3 2
    copy 3 1
    add # 128 in reg 3
    copy 3 1
    copy 3 2
    add 
    copy 3 6
    # total 256 """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert to_int(cpu.reg.output) == 0, f"cpu.reg.output should be zero due to overflow: {cpu.reg.output}"
    assert to_int(cpu.reg.registers[2]) == 128
    
    cpu = CPU(program[:-1]) # dont run the copy out to maintain alu state
    cpu.run()
    assert cpu.alu.overflow == cpu.alu.zero == True, cpu.alu #TODO should thi carry out be high here?


def test_sub_math():
    code = """
    2
    copy 0 2
    sub  # 0 - 2 = -2
    copy 3 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert cpu.reg.output == [1,1,1,1,1,1,1,0], cpu.reg.output
    # assert to_int(cpu.reg.output) == -2, f"cpu.reg.output should be zero due to overflow: {cpu.reg.output}" #to int doesnt do negative

def test_add_sub_math():
    code = """
    32
    copy 0 1
    32
    copy 0 2
    add  # 64 in reg 3
    copy 3 2
    copy 3 1
    add # 128 in reg 3
    1
    copy 0 2
    copy 3 1
    sub     # 128 - 1
    copy 3 6
    """
    program = assemble_binary(code_string=code)
    cpu = CPU(program)
    cpu.run()
    assert cpu.reg.output == [0,1,1,1,1,1,1,1] 
    assert to_int(cpu.reg.output) == 127