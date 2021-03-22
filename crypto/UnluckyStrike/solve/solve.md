At heart this is just a padding oracle challenge. But it always throws at you a corner case, so the 
usual just retry and it will work lazy approach will not work. It is not immediately evident why this 
is so, nothing is suspicious in the public source code. Check proprietary_data.py to see the 
sheenanigans :)

The naive solver (naive_solver.py) chokes on this. But a more careful one (sol.py) 
gets the flag.

I would rate it at 4 in difficulty   (1 easy, 3 mid, 5 hard).



