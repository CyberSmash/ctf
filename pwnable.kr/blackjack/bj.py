from pwn import *
import re

score_regex = r"Your Total is ([0-9]+)"
c_score_regex = re.compile(score_regex)

def get_score(data, reg):
    m = re.search(reg, data)
    return m.group(1)
    
def main():

    r = remote('localhost', 2020)
    data = r.recvuntil('(Y/N)', drop=True)
    print(data.decode())
    r.sendline(b"Y")
    data = r.recvuntilS("Choice")
    r.sendline(b"1")
    data = r.recvuntilS("Enter Bet: $")
    score = get_score(data, c_score_regex)
    print(f"Current Score: {score}")

if __name__ == "__main__":
    main()
