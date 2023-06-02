# 1 = turn left, 2=  turn right, 3=  step forward
# we will store info about left in reg4, info about right in reg5

label uturn
2
copy 0 6

label right
2
copy 0 6
copy 0 6

label left
1
copy 0 6

label ahead
3
copy 0 6

label start
# check if wall to the left store in 3
1
copy 0 6
copy 6 3
2 
copy 0 6

#if no wall left, turn left until there is a wall
left 
eval =

# there is a wall left, check ahead
copy 6 1
# check right
2
copy 0 6
copy 6 2
1 
copy 0 6
# if wall ahead and right do a uturn
and
uturn
eval !=

# if wall ahead but no wall right turn right
copy 1 3
right
eval !=

ahead
eval always 
