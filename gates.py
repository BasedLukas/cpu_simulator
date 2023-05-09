

def and_(a:bool, b:bool)->bool:
    return a & b

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



