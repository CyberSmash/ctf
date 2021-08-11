from pwn import *

#a_addr = 0x0809fe4b
#b_addr = 0x0809fe4b

#r = remote('localhost', 2020)
str = 'A' * 120
g = gdb.debug('./horcruxes')

