#!/usr/bin/env python


import subprocess
import struct


pipe = subprocess.PIPE

def pkiller():
    from ctypes import cdll
    import ctypes
    # PR_SET_PDEATHSIG, SIG_KILL --> kill child when parent dies
    cdll['libc.so.6'].prctl(1, 9)


def test(fname, out):
    print("="*5, "testing " + fname)
    p = subprocess.Popen(["./boiledvm.py"], stdout=pipe, stderr=pipe, stdin=pipe, close_fds=True, preexec_fn=pkiller)

    with open(fname, "rb") as fp:
        cc = fp.read()
    res = []
    try:
        ro,e = p.communicate(cc, timeout=1.5)
        print(ro)
        t = False
        o = ro.split(b"\n")[-2]
        try:
            o = int(o.split()[-1])
        except ValueError:
            o = ro.strip()
    except subprocess.TimeoutExpired:
        o = 0
        e = b""
        t = True
    res = [o,e,t]
    print(repr(res))

    assert res[0] == out[0]
    assert res[1] == out[1]
    assert res[2] == out[2]


test("i2.txt", [0x67,b"",False])
test("i3.txt", [14,b"",False])
test("i1.txt", [0,b"",True])
test("i4.txt", [0x6688aacc,b"",False])
test("i5.txt", [0x11+0x77,b"",False])
test("i8.txt", [0x11*0x7,b"",False])
test("i9.txt", [0x11*9,b"",False])

test("i11.txt", [b"Welcome to the boilervm!\nhow many instructions? how many values? Invalid register number!", b"", False])
test("i12.txt", [b"Welcome to the boilervm!\nhow many instructions? how many values? Invalid register number!", b"", False])
test("i13.txt", [b"Welcome to the boilervm!\nhow many instructions? how many values? Invalid register number!", b"", False])
test("i14.txt", [b"Welcome to the boilervm!\nhow many instructions? how many values? Invalid jump target!", b"", False])

with open("flag", "rb") as fp:
    ff = fp.read()
ff = ff.strip()[:8]
test("i10.txt", [struct.unpack("<Q", ff)[0],b"",False])
with open("flag", "rb") as fp:
    ff = fp.read()
ff = ff.strip()[8:16]
test("i20.txt", [struct.unpack("<Q", ff)[0],b"",False])

print("="*5, "test with socat")
p = subprocess.Popen(["./test_with_socat.sh"], stdout=pipe, stderr=pipe, stdin=pipe, close_fds=True, preexec_fn=pkiller)
res = p.communicate()
print(res[0])
assert ff in res[0]

print("="*10, "ALL GOOD!")

'''
./rebuild.sh
./test.py
'''
