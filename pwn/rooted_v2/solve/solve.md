# SOLVE:

This challenge is a rehash of the old jail with a twist of a "little" more challenging binary.


## analysis up to code:
see rooted\_v1\solve\solve.md for grabbing the code.
Lets check the security of the elf file with pwntools checksec utility:
```
$ checksec test
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
Hmmm looks like NX is enabled now, so maybe our shellcode won't work?

Once we have the code we can pop the code into ghidra and checkout the decompiled version,
same as before ghidra gives us a super clean output:
```c
undefined8 main(void)

{
  __gid_t __rgid;
  char *__s;
  size_t sVar1;
  int local_30;
  byte local_1d;
  
  setvbuf(stdout,(char *)0x0,2,0);
  __rgid = getegid();
  setresgid(__rgid,__rgid,__rgid);
  __s = (char *)mmap((void *)0x0,0xfa,6,0x22,-1,0);
  puts("HI ADMIN :) YOUR CODE IS SETUP, WHAT DO YOU WANT ME TO PRINT?");
  fgets(__s,0xfa,stdin);
  sVar1 = strlen(__s);
  local_30 = 0;
  while (local_30 < (int)sVar1) {
    local_1d = __s[local_30] ^ 0x58;
    if ((local_1d != 0x41) && (local_1d != 0x42)) {
      local_1d = 0x41;
    }
    if (local_1d == 0x41) {
      opt_a(__s);
    }
    else {
      if (local_1d == 0x42) {
        opt_b(__s);
      }
    }
    local_30 = local_30 + 1;
  }
  return 0;
}
```
We can see here its similar to the previous challenge, but now with a modified twist!
First the binary calls mmap with a bunch of weird inputs...  how can we figure out the flags that were passed in and determine how this memory is initialized? We'll dive into that here after investigating the rest of the binary. 
Once that memory is mapped and set, a string is read in, then a loop goes over each index of the string (at least as far as the length found from strlen). Each byte of the input is xor'd with 0x58 and is set to 0x41 if the result is not 0x41 ('A') or 0x42 ('B'). 
Then if the results is 'A' it runs the `opt\_a` function or 'B' it runs `opt\_b` function.
`opt_a` isn't interesting it just prints, but `opt_b`:
```c
void opt_b(undefined *param_1)

{
  puts(&DAT_00402012);
  (*(code *)param_1)();
  return;
}
```
sweet it looks like opt\_b will run whatever code is in our buffer! So now we just need to check out what mmap is doing!

Looking at `man mmap` we see the arguments passed in are the default address, the size of the mapped region, protection flags, other flags, fd and length. Since file descriptor and length are zero, its safe to assume this mapping is a region of memory allocated for the process. 
So now we want to check what protections the memory region has by determining what flags 0x22 corresponds to. 

We can checkout some local files on the linux os to figure that out, luckily we know that the remote server is running on ubuntu, and our local system is ubuntu so we can safely guess that whatever our header files define these values as the remote server probably does as well. (Theres a good possibility this is generic across all linux systems, but I truly don't know). 

To explore this question, we need to first navigate to the header files directory that the c compiler utilizes. They are located in `/usr/include`. We know from the man page of mmap that the flags are defined as **PROT_EXEC** PROT\_WRITE**, so next its time to use the good old `grep` method:
```bash
cd /usr/include
grep -r "define" . | grep PROT_EXEC
./x86_64-linux-gnu/bits/mman-linux.h:#define PROT_EXEC  0x4             /* Page can be executed.  */
./asm-generic/mman-common.h:#define PROT_EXEC   0x4             /* page can be executed */
```
so now we have our file, if we open it up we find that 6 must be the addition of *PROT_WRITE* and *PROT_EXEC*! (Looks like thats similar to linux file permissions!) So this page is both Exectuable and Writable! Looks like our shellcode will be good to go!

However we have an issue, in order to actually get our shellcode to execute it requires that we have some byte that xors with 0x58 into 0x42 ('B'). We can run some quick python to reverse the xor:
```python3
>>> hex(0x42 ^ 0x58)
'0x1a'
```
Looks like we need to have an '0x1a' byte in our shellcode somewhere, an easy way to do this is just to add a jump instruction into the beginning of our shellcode to skip over the 0x1a byte. So this is what we add to the beginnig of the shellcode:
```asm
jmp x 
;PLACE HOLDER, we need to add a byte manually here
x:
  push 83
	;GO ON:
```

This then gives us a jmp 0 instruction in the output, which we can edit manually in our final shellcode bytes.
```
eb 00 => eb 01 1a
``` 
This gets our 1a byte into the shellcode, but also skips its execution!


Now lets let our modified shellcode rip in our updated pwn script! (We also had to change the string to match the output!):
```
$ python3 solve.py
[+] Opening connection to chal.ctf.b01lers.com on port 7002: Done
b'bctf{5h311c0d3_20ck5_50ck5}'
```

## Conclusion:
	Hope this challenge was fun and a little bit more difficult than the last! Had a ton of fun creating these and I hope I can create more challenges into the future!


