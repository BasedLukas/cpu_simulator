

# def and_(a:bool, b:bool)->bool:
#     return a & b

def and_(*args:bool)->bool:
    return all(args)

def or_(a:bool, b:bool)->bool:
    return a | b

def xor(a:bool, b:bool)->bool:
    return a ^ b

def not_(a:bool)->bool:
    return not a

def nor(a:bool, b:bool)->bool:
    return not or_(a, b)

def nand(a:bool, b:bool)->bool:
    return not and_(a, b)

def xnor(a:bool, b:bool)->bool:
    return not xor(a, b)




# def bit_and(params: list[bool]) -> bool:
#     assert len(params) > 1 # At least two inputs are required
#     return True if all(params) else False

# def bit_or(params: list[bool]) -> bool:
#     assert len(params) > 1 # At least two inputs are required
#     return True if any(params) else False

# def bit_not(params: list[bool]) -> list[bool]:
#     assert len(params) > 1 # At least two inputs are required
#     return [not x for x in params]

# def bit_nand(params: list[bool]) -> bool:
#     assert len(params) > 1 # At least two inputs are required
#     return not bit_and(params)

# def bit_nor(params: list[bool]) -> bool:
#     assert len(params) > 1 # At least two inputs are required
#     return not or_(params)
