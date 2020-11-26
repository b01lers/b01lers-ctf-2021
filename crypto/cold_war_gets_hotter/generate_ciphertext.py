#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad 


key = open('key', 'rb').read()

purdue_coordinates = b'38.9,-86.3'

plaintext = open('plaintext', 'rb').read()

initial = 51 * 16 + 4

plaintext = plaintext[:initial] + purdue_coordinates + plaintext[initial:]

cipher = AES.new(key, AES.MODE_CBC)
cipherText = cipher.encrypt(pad(plaintext, AES.block_size))


print(cipher.iv.hex(), cipherText.hex(), sep='')
