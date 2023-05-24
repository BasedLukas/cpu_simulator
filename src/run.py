from cpu import CPU



program1 = [
        # MOVE 3 into reg0
        [0,0,0,0,0,0,1,1],
        # copy into reg 1
        [1,0,0,0,0,0,0,1],
        #move 5 into reg0
        [0,0,0,0,0,1,0,1],
        #copy into reg2
        [1,0,0,0,0,0,1,0],
        #add reg1 and reg2 and store in reg3
        [0,1,0,0,0,0,0,0],
        
        ]



cpu = CPU(program1)
cpu.run()