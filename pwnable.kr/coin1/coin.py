from pwn import *
import re

num_and_tries_re = r"N=([0-9]+) C=([0-9]+)"
num_and_tries_re_c = re.compile(num_and_tries_re)

HAS_CF = 1
NO_CF = 2
CORRECT = 3
INCORRECT = 4
CORRECT_RETRY = 5

def get_banner(r, verbose=False):
    banner = r.recvuntilS("3 sec... -")
    if verbose:
        print(banner)


def get_setup(r, verbose=False):
    data = ''
    while len(data) == 0:
        data = r.recvlineS().strip()

    if verbose:
        print(data)
    if data.find("Congrats") > -1:
        print(r.readlineS(timeout=1))
        print(r.readlineS(timeout=1))
        print(r.readlineS(timeout=1))
    m = re.search(num_and_tries_re_c, data)
    if verbose:
        print(f"Number of coins {m.group(1)}")
        print(f"Number of tries {m.group(2)}")

    return int(m.group(1)), int(m.group(2))

def test_list(r, coins, verbose=False):
    str_coins = [str(i) for i in coins]
    coin_str = ' '.join(str_coins)
    if verbose:
        print(f"Sending: {coin_str}")
    r.sendline(coin_str)
    data = r.readlineS().strip()
    if verbose:
        print(f"List test Response: {data}")

    return data
    
def check_test_response(response, verbose=False):
    if verbose:
        print(f"Parsing: {response}")
    if response.isdigit():
        val = int(response)
        if val % 10 == 0:
            return NO_CF
        elif val == 9:
            return CORRECT_RETRY
        return HAS_CF
    if response.find("Correct!") > -1:
        return CORRECT
    return INCORRECT

def handle_response(r, coins, verbose=False):

    print(f"--- Current coin range: {coins} ---")
    halfwaypoint = len(coins) // 2
    if halfwaypoint == 0:
        response = test_list(r, coins, True)
    else:
        coin_first_half = coins[:halfwaypoint]
        coin_second_half = coins[halfwaypoint:]
        response = test_list(r, coin_first_half, True)
    
    response_type = check_test_response(response, True)
    if response_type == HAS_CF: 
        print(f"Coin in first_half")
        handle_response(r, coin_first_half)
    elif response_type == NO_CF:
        print(f"Coin in second_half")
        handle_response(r, coin_second_half)
    elif response_type == CORRECT:
       print("Correct! Coin is coins[0]")
    elif response_type == INCORRECT:
        print("We got it wrong ... hmm ...")
    elif response_type == CORRECT_RETRY:
        # we have found the coin, but too early. Just send it again.
        handle_response(r, coins, verbose)

def main():
    r = remote('localhost', 2020)
    get_banner(r, True)

    while True:
        num_coins, num_chances = get_setup(r, True)
        coins = range(0, num_coins)
        handle_response(r, coins, True)
               
    return

if __name__ == "__main__":
    main()
