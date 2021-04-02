from binascii import hexlify
import random
import os

challenges = ['./chals/chal1', './chals/chal1a', './chals/chal1b', './chals/chal2', './chals/chal2a', './chals/chal2b', './chals/chal3', './chals/chal3a', './chals/chal3b']

while len(challenges):
    binary = random.choice(challenges)
    challenges.remove(binary)

    print("Binary: ")
    with open(binary, 'rb') as f:
        print(hexlify(f.read()))

    os.system(binary)
    # TODO: Check mini-flag, abort if not available


print('Success, here is the flag: flag{yeet}')  # TODO: Flag
