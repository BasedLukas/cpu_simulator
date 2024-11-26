import pytest
from io import StringIO, BytesIO

from assembler.assembler import assemble_binary



def test_comments():
    program = assemble_binary("tests/comments.asm")
    assert program[0] == [1,0,0,0,0,0,0,1] # == copy 0 1
    assert len(program) == 3


def test_invalid():
    with pytest.raises(Exception):
        assemble_binary("tests/invalid_1.asm")
        assemble_binary("tests/invalid_2.asm")


def test_label():
    with pytest.raises(Exception):
        # test no labels after 64 limit
        assemble_binary('tests/label_overflow.asm')
        
        # test double labels 
        assemble_binary('tests/double_labels.asm')

    #test comments and labels dont increase count
    assemble_binary('tests/label_not_overflow.asm')


def test_copy():
    # Test valid copy instructions
    program = assemble_binary("tests/copy_valid.asm")
    assert program == [
        [1, 0, 0, 0, 0, 0, 0, 1],  # copy 0 1
        [1, 0, 0, 1, 0, 0, 1, 1],  # copy 2 3
        [1, 0, 1, 0, 0, 1, 0, 1],  # copy 4 5
        [1, 0, 1, 1, 0, 0, 0, 0],  # copy 6 0
    ]
    with pytest.raises(Exception):
        assemble_binary("tests/copy_too_few_args.asm")
        assemble_binary("tests/copy_out_of_range.asm")
        assemble_binary("tests/copy_invalid_format.asm")



def test_basic_assembly():
    assemble_binary("src/program.asm")
