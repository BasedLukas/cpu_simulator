
def and_(*args:bool)->bool:
    return all(args)

def or_(*args:bool)->bool:
    return any(args)

def not_(*args:bool)->bool:
    return not all(args)

def nor(*args:bool)->bool:
    return not_( or_(*args) )

def nand(*args:bool)->bool:
    return not_( and_(*args) )


def xor(a:bool, b:bool)->bool:
    return a ^ b


def xnor(a:bool, b:bool)->bool:
    return not xor(a, b)