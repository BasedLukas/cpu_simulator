
1 # put 1 in reg0
copy 0 1 # copy reg0 to reg1

label start_loop
add # add reg 1 and 2
copy 3 2 # copy result into reg2

copy 3 6 # print result
# loop so long as result is >= 0 (using signed nums)
start_loop
eval >=



