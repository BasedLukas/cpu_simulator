2               #turn right twice
copy 0 6
copy 0 6  
10             # jump to start
eval always     
2               # start right (5)
copy 0 6        
copy 0 6        
1                # start left (8)
copy 0 6        
3               # start (move forward) (10)
copy 0 6        #...
2               #...
copy 0 6        #check r into reg4
copy 6 4
1
copy 0 6        #...
1               #...
copy 0 6        #   
copy 6 3        #   check left into 3
2               #
copy 0 6        #..
copy 6 0        # ahead in 0
copy 4 1        # r in 1
and
copy 3 0
copy 2 1        # we are in a dead end
and
0               # so turn right
eval !=         #..
1               #...
copy 0 6        #   
copy 6 3        #   check left into 3
2               #
copy 0 6        #...
copy 6 1        #
copy 3 0        # wall left and ahead
and             #
5               #
eval !=         #...
1               #
copy 0 6        # 
copy 6 3        # if wall left
2
copy 0 6
10
eval !=        #...
8              # If no wall left then start left
eval always    #...






