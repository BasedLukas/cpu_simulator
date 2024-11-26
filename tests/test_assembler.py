import pytest

from assembler.assembler import assemble_binary



def test_comments():
    comments = """
                # copy 2 3
                # copy 1 2
                # copy 4 5
                # copy 3 4


                # copy 0 1
                # copy 5 6
                # copy 0 1


                # copy 0 1
                # copy 0 1
                # copy 0 1
                copy 0 1 # comment here not included in file, instruction included
                # copy 0 1

                # copy 0 1
                # copy 0 1
                # copy 0 1
                copy 2 5

                copy 5 2
                # copy 0 1
                # copy 0 1
                # label first
                # copy 0 1
                # copy 0 1
                # copy 0 1
                # copy 0 1
                # copy 0 1
                # copy 0 1
                # copy 0 1
                # label first
                # copy 0 1
                """
    program = assemble_binary(code_string=comments)
    assert program[0] == [1,0,0,0,0,0,0,1] # == copy 0 1
    assert len(program) == 3


def test_invalid():
    # Test invalid instructions with incorrect formats
    invalid_instructions = """
    # Invalid 'copy' instructions due to incorrect format
    Copy 0 1     # 'Copy' should be lowercase
    cop 0 1      # Misspelled instruction
    copy 0 1 2   # Too many arguments
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=invalid_instructions)

    # Test instructions with numbers out of range
    out_of_range = """
    # Invalid 'copy' instructions with numbers out of valid range
    copy 7 0
    copy 0 8
    copy -1 3
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=out_of_range)

    # Test instructions with too few arguments
    too_few_args = """
    # Invalid 'copy' instructions with too few arguments
    copy 1
    copy
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=too_few_args)


def test_label():
    # Test exceeding the label limit
    label_overflow = """
    # Exceeding the label limit with more than 64 instructions
copy 1 2
copy 2 3
copy 3 4
copy 4 5
copy 5 6
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
label after_limit
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=label_overflow)

    # Test duplicate labels
    double_labels = """
    copy 1 2
    copy 2 3
    label first
    copy 3 4
    label first  # Duplicate label 'first'
    copy 4 5
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=double_labels)

    # Test labels within limit and ensure comments don't count towards limit
    label_not_overflow = """
copy 1 2
copy 2 3
copy 3 4
copy 4 5
copy 5 6
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
copy 0 1
label a 
label b
label c
label d  
label e
label f
label g
label h
# copy 0 1
# copy 0 1
# copy 0 1
# copy 0 1
# copy 0 1
# copy 0 1
# copy 0 1
label after_limit
    """
    # This should not raise an exception
    assemble_binary(code_string=label_not_overflow)


def test_copy():
    # Test valid 'copy' instructions
    valid_copy_instructions = """
    copy 0 1
    copy 2 3
    copy 4 5
    copy 6 0
    """
    program = assemble_binary(code_string=valid_copy_instructions)
    assert program == [
        [1, 0, 0, 0, 0, 0, 0, 1],  # 'copy 0 1'
        [1, 0, 0, 1, 0, 0, 1, 1],  # 'copy 2 3'
        [1, 0, 1, 0, 0, 1, 0, 1],  # 'copy 4 5'
        [1, 0, 1, 1, 0, 0, 0, 0],  # 'copy 6 0'
    ]

    # Test 'copy' instructions with too few arguments
    copy_too_few_args = """
    copy 1
    copy
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=copy_too_few_args)

    # Test 'copy' instructions with numbers out of range
    copy_out_of_range = """
    copy 7 0
    copy 0 8
    copy -1 3
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=copy_out_of_range)

    # Test invalid 'copy' instruction formats
    copy_invalid_format = """
    Copy 0 1     # 'Copy' should be lowercase
    cop 0 1      # Misspelled instruction
    copy 0 1 2   # Too many arguments
    """
    with pytest.raises(Exception):
        assemble_binary(code_string=copy_invalid_format)


def test_basic_assembly():
    # test copy
    code = """
    # Basic assembly code example
    copy 0 1
    copy 6 2
    copy 2 6
    """
    program = assemble_binary(code_string=code) 
    assert len(program) == 3

    # immediate values
    code = """
    1
    2
    63    
    """
    program = assemble_binary(code_string=code)
    assert len(program) == 3

    # eval
    code = """
    1
    eval >
    3 
    eval never
    """
    program =assemble_binary(code_string=code)
    assert len(program) == 4

    #label
    code = """
    label start
    3
    copy 1 2
    start
    eval =
    """
    program = assemble_binary(code_string=code)
    assert len(program) == 4