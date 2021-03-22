# VM exploitation

You can send instructions to a VM that is first compiling them and then executing them

The instructions are in a very minimalistic, Turing-complete language.

There are two components a Python component and a child process executing the compiled instructions.

The Python component supervises the execution of the child process, and it checks the validity of some array bounds using ptrace.

It is possible to trigger a SIGSEV exception in the child component that is handled incorrectly by the Python component, leading to arbitrary code execution inside the child process.

`src/test.py` executes different tests.s
`src/i10.txt` is the input that when provided to the program leaks the flag.

The flag cannot be longer than 8 bytes, therefore I am not following the standard flag format.

