; thanks to https://www.muppetlabs.com/~breadbox/software/tiny/teensy.html

 BITS 32
  
                org     0x08048000
  
  ehdr:                                                 ; Elf32_Ehdr
                db      0x7F, "ELF", 1, 1, 1, 0         ;   e_ident
        times 8 db      0
                dw      2                               ;   e_type
                dw      3                               ;   e_machine
                dd      1                               ;   e_version
                dd      _start                          ;   e_entry
                dd      phdr - $$                       ;   e_phoff
                dd      0                               ;   e_shoff 
                dd      0                               ;   e_flags
                dw      ehdrsize                        ;   e_ehsize
                dw      phdrsize                        ;   e_phentsize
                dw      1                               ;   e_phnum
                dw      0                               ;   e_shentsize
                dw      0                               ;   e_shnum
                dw      0                               ;   e_shstrndx
  
  ehdrsize      equ     $ - ehdr
  
  phdr:                                                 ; Elf32_Phdr
                dd      1                               ;   p_type
                dd      0                               ;   p_offset
                dd      $$                              ;   p_vaddr
                dd      $$                              ;   p_paddr
                dd      filesize                        ;   p_filesz
                dd      filesize                        ;   p_memsz
                dd      5                               ;   p_flags
                dd      0x1000                          ;   p_align
  
  phdrsize      equ     $ - phdr
  
  _start:
      mov DWORD[esp], 0
      mov DWORD[esp-4], 0
      mov DWORD[esp-8], 0

      ; accept 1 character
      mov DWORD[esp], 0
      mov edx, 1
      mov ecx, esp
      mov ebx, 0
      mov eax, 3
      int 0x80

      write_result:
      ; XOR current flag byte with input byte
      movzx edx, BYTE[esp-4]
      movzx ecx, BYTE[flag + edx]
      movzx edx, BYTE[esp]
      xor ecx, edx
      mov [esp-8], ecx

      ; write it to stdout
      mov     edx,1
      mov     ecx,esp
      sub ecx, 8
      mov     ebx,1
      mov     eax,4
      int 0x80

      ; check if finished
      mov ecx, [esp-4]
      inc ecx
      mov [esp-4], ecx
      cmp ecx, flaglen
      jl write_result

      ; exit
      mov     ebx,0
      mov     eax,1
      int 0x80

      flag db    0x0, 0x1, 0x16, 0x4, 0x19, 0xf, 0x53, 0xc, 0x51, 0x1, 0x10, 0x3, 0x56, 0x4, 0x16, 0x3d, 0x27, 0x2e, 0x24, 0x1, 0x10, 0x56, 0x4, 0x16, 0x1f
      flaglen equ     $ - flag


filesize      equ     $ - $$
