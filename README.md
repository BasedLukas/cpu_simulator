
# 8 bit CPU emulator

The goal is to simulate an 8 bit CPU using only logic gates and building upwards. All the operations should be based on the properties of the logic gates, and changing their function should lead to corresponding changes in function.   


tests.py should run error free.  
run.py gives you a basic cpu.

The individual components are based 100% on the operation of the logic gates defined in gates.py - changing functionality there will effect everything downstream.

You can write a program in binary or use the assembler and write one in assembly.

# Design

There are 6 registers, an input and an output. There are 4 recognized operations; 
### Immediate, Operate, Copy and Eval
```
00 = immediate   
01 = operate (add, subtract, and, or)   
10 = copy (source, destination)   
11 = eval
```

#### Immediate
Moves the byte (from the program) into reg0.
```
00 000 000 : move 0 into reg0   
00 000 011 : move 3 into reg0
```   
Notice that the 2 MSB must always be false

#### Operate
The 2 LSB in the instruction determine which operation is performed as follows;  
```
control1 | control2
       0 | 0        | Add  
       0 | 1        | Or  
       1 | 0        | Subtract   
       1 | 1        | And

01 0000  00  : Add  
01 0000  01  : Or  
```
The operands are always reg1 and reg2 and the output is stored in reg3.

#### Copy  

3 bits for the source and 3 bits for the destination
```
01 000 001 : copy from reg0 to reg1  
01 110 101 : copy from input to reg5
```
#### Eval
Evaluates reg3 against a condition, if true sets the program counter to the value in reg0.

USES SIGNED NUMBERS 10000000 = -128  

    cntrl | byte value | output
    ___________________________
    000   | any        | false
    001   | =0         | true
    010   | <0         | true
    011   | <=0        | true
    100   | any        | true
    101   | !=0        | true
    110   | >=0        | true
    111   | >0         | true

```
11 000 000 : will do nothing  
11 000 100 : will always update  
11 000 111 : will update if reg3 > 0
```
The program counter starts on zero and inrements by one for each operation.

#### Example program
```
3  
copy 0 1  
5  
copy 0 2  
add  
#loop  
0  
eval 111
```
This will put 3 in reg0  
copy 3 to reg1  
put 5 in reg0  
copy 5 to reg2  
add 5+ 3 and store in reg3  
put 0 in reg0  
if 8 > 0 then start the program again from instruction 1


# Other


The entire project is still work in progress. The assembler still needs some work too.
In the docs folder are schematics of how some of the components operate.
