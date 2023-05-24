# cpu simulator  

The goal is to simulate an 8 bit CPU with a von Neumann type architecture using only logic gates and building upwards.  
All the operation should be based on the properties of the logic gates, and changing their function should lead to corresponding changes in opperation.  
Check out the docs for details.  
tests.py should run error free.  
run.py gives you a basic cpu.  
the basic components and ALU are all 100% authentically based on the operation of the gates. the cpu curretly stil makes use of python if statements, but that will e rectified shortly.  

the entire project is still work in progress.

# Instruction set

Instruction set
00 = Immediate
01 = operate (add, subtract, and, or)
10 = copy (source, destination)
11 = Edit program counter/ ram (TODO)

IMMEDIATE:
moves the number into reg0, example:
00 000 000 = move 0 into reg0
00 000 001 = move 1 into reg0
notice that the 2 MSB must always be false

OPERATE:
2 LSB determine operation as per alu specs
always operates on reg1 and reg2 and stores in reg3
ALU rules;
    control1 | control2
    0        | 0        = Add
    0        | 1        = Or
    1        | 0        = Subtract
    1        | 1        = And

COPY:
3 bits determine source register, next 3 bits determine destination register. 
110 refers to input or output

10 000 010 = move from reg0 to reg2
10 000 110 = move from reg0 to out 
10 110 000 = move from input to reg0


# demo program

program1 = [
        # MOVE 3 into reg0
        [0,0,0,0,0,0,1,1],
        # copy from reg0 into reg 1
        [1,0,0,0,0,0,0,1],
        #move 5 into reg0
        [0,0,0,0,0,1,0,1],
        #copy from reg0 into reg2
        [1,0,0,0,0,0,1,0],
        #add reg1 and reg2 and store in reg3
        [0,1,0,0,0,0,0,0],
        
        ]
