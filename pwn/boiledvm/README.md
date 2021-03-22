# boiledvm

The user send instructions to a VM that is first compiling them to x86 and then executing them.

The instructions are in a very minimalistic, Turing-complete language.

There are two components a Python component and a child process executing the compiled instructions.

The Python component supervises the execution of the child process, and it checks the validity of some array bounds using ptrace.

It is possible to trigger a SIGSEV exception in the child component that is handled incorrectly by the Python component, leading to arbitrary code execution inside the child process.

`src/test.py` executes different tests.

`src/i10.txt` is the input that when provided to the program leaks the flag.

Due to the nature of the VM communication and its exploitation it is hard to have a flag cannot longer than 8 bytes (and a flag file name longer than 4 characters), therefore I am not following the standard flag format.

