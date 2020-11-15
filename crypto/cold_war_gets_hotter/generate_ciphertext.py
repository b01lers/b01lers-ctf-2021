#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad 


key = open('key', 'rb').read()

plaintext = b'''"Indiana, Our Indiana"

Indiana, our Indiana
Indiana, we're all for you!
We will fight for the cream and crimson
For the glory of old IU
Never daunted, we cannot falter
In the battle, we're tried and true
Indiana, our Indiana,
Indiana we're all for you! I-U!

"Indiana Fight"

Fight for the Cream and Crimson,
Loyal sons of our old I. U.
Fight for your Alma Mater,
and the 39.1,-86.5school you love so true.
Fight for old Indiana,
See her victories safely through,
GO! I.U! FIGHT! FIGHT! FIGHT!
For the glory of old I. U.!
'''

cipher = AES.new(key, AES.MODE_CBC)
cipherText = cipher.encrypt(pad(plaintext, AES.block_size))


print(cipher.iv.hex(), cipherText.hex(), sep='')
