#!/usr/bin/env python3

from pwn import remote, context
import binascii
host = '127.0.0.1'
port = 25000

context.log_level = 'debug'

conn = remote(host, port)

ciphertext = open('ciphertext', 'r').read()


def xor_block(a, b):
    return [a[x] ^ b[x] for x in range(len(a))] 

iu_coordinates = b'39.1,-86.5'
purdue_coordinates = b'38.9,-86.3'
base_xor = xor_block(iu_coordinates, purdue_coordinates)

attempts = 0


def get_block(source, block_num):
    return source[block_num * 32: (block_num + 1) * 32]

def get_blocks(source, block_num):
    return get_block(source, block_num), get_block(source, block_num + 1)

def generate_xor_source(base, prepend):
    new_base = ([0] * prepend) + base
    return new_base + ([0] * (16 - len(new_base)))

def alter_block(orig, xor_source):
    orig_bytes = binascii.unhexlify(orig)
    xored = xor_block(orig_bytes, xor_source)
    return binascii.hexlify(bytearray(xored)).decode()


def receive_until_prompt(r):
    return r.recvuntil('> ')

def send_text(r, text):
    r.sendline(text)

def check_success(response):
    if b'Coordinates have not been altered' not in response:
        print(response)
        print(attempts)
        exit(0)


receive_until_prompt(conn)
for block in range((len(ciphertext) // 32) - 1):
    first, second = get_blocks(ciphertext, block)
    for i in range(16 - len(base_xor)):
        send_text(conn, b'2')
        
        shifted = generate_xor_source(base_xor, i)
        altered = alter_block(first, shifted)
        send_text(conn, altered + second)
        
        y = receive_until_prompt(conn)
        check_success(y)
        attempts += 1

    
print("unsuccessful :(")
    

