#!/usr/bin/env python

import sys
import os
import socket
import struct


IP = sys.argv[1]
PORT = int(sys.argv[2]) #7012

with open("../src/i10.txt", "rb") as fp:
    cc = fp.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP, PORT))
s.sendall(cc)

buf = b""
while True:
    tbuf = s.recv(1024)
    if len(tbuf) == 0:
        break
    buf += tbuf

flag_enc = buf.strip().split()[-1]
flag = struct.pack("<Q", int(flag_enc, 10))
print("FLAG:", flag.decode("utf-8"))

#./solve.py <ip> 7012
