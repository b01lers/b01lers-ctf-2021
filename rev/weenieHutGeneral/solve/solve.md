# Solution for: Weenie Hut General
## Concept:
This challenge is a C shared object file (a library). With this we're testing decompilation and being able to compile a C file with a shared object (.so) file.

## Solve:
To start, take the .so file and open it in a decompiler, such as Ghidra. Inside you'll find three major functions. One is the main function which calls a subfunction and then has an if/else chain to check the input. 

In the subfunction, you'll see a call to srand with a specific seed. Back in the calling function you'll see that rand() is used twice. So now that you have the seed you can know what the first two calls of rand() will produce. 

Next you'll see that the input is bitwise XORd with 0x98c3a78b, then rand(), then 0xad5410ca. The output is of that will equal the next rand(). To find the desired input, do a bitwise XOR of each of the other values (the two hex values and the two rands()) and that will give you your input!

To test if the input you got is correct, you need to compile a C file that calls the previously mentioned calling function, called "tryToRev(int input)". To do this you need to include "extern void tryToRev(int);" as a header in your C file. Then in your main function you can call "tryToRev(number)". 

When compiling with a .so file, do not forget to include the path to the so file in your PATH!

If the answer is correct, you will get a statement that the flag is the input!
