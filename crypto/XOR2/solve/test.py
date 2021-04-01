ctxt = open("chal2.enc", "rb").read()

key1= b'\x94\x9a\\\xf2B\xf1\xe1\xa6i\xe9\x18\x96k\x17\x97\xf5WDbw-\x03\\\r&\x8f+:\xa1-B\xd1\xbf-\xb98\xf5N\xc7>\xa4\x8a\xe8C\xd4E.2; \xc8\xf5\x9b'
key2= b'\xd5\xb6,EQI=\xee](\x86Q\xbb\x00\xce\xc3\x1a\xb2\x96]s\x9c\xdb\xec\x98\xd5\xba\x05W\xdb\x8b\x92;\xfa\x8a\xcb\x81\x1fy[\x0e\xe9\xab\xa3\xad~3\xff\xf0\x18\xaf?\xb7\xd6v\xf24\xff4?\x8c\x8b\xf75\xb9\x9bP\xd6%\x81\xcc'


def xor(msg, key):
   nkey = len(key)
   return bytes( [ msg[i] ^ key[i % nkey]   for i in range(len(msg))] )


ptxt = xor(ctxt, key1)
ptxt = xor(ptxt, key2)
print(ptxt)

