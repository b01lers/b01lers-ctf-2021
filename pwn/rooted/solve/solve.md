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
**TODO FINISH**
important commands

```
ls ... other command testing
echo *
echo .*
echo $(<.admin_check)
```

## Shellcode Time
Pre reqs:
```
sudo apt install nasm
```

Run the following
``` bash
#write shellcode into shellcode.asm
nasm -f elf64 shellcode.asm -o shellcode.o
ld shellcode.o -o shellcode
objdump -d shellcode
#highlight middle column bytes and place into shell.py
python3 shell.py | xclip -selection clipboard
# test
gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
```


#### Side Note:
I actually wrote this while solving the challenge myself haha
hope others found the challenge fun and interesting, I certainly learned alot while making it!

#### Side Note 2:
peda is great, if you want to intall it: 
```bash
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
echo "DONE! debug your program with gdb and enjoy"
```




