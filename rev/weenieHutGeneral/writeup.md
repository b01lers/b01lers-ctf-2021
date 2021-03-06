## Weenie Hut General
# Author: NikMaybe
Point value: 200

Weenie Hut General is secured with a passcode so only employees can get in. Your first shift starts and you can't remember the code! The system is managed using this shared object file. Can you crack the code before you get demoted to weenie hut junior?

Solve:
Open the file in your favorite decompiler (ex. Ghidra).

Search the functions until you find the one that does the input validation and checking.

But where is the rand coming from? Check the first function called, the rand seed is set there.

Solve the input validation equation for the input and that's your flag!


