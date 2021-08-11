#!/usr/bin/env python3
from pwn import *

#s = ssh(host='localhost', port=2020, user='uaf', password='guest')
#s.interactive()
g = gdb.debug(target='./uaf', gdbscript='''
break *0x0000000000400f05
break *0x0000000000400f63
break *0x0000000000401025
run 24 ./abcd.txt
''')
g.interactive()
