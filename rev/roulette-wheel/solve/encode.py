#snippet for turning the flag into chunks that
# won't easily be grabbed with the strings command
flag = "MJRXIZT3GRVWQYRUGRZDCNJUNUYHEMDOPUFA====" #"bctf{4khb44r154m0r0n}"
i = 0
for f in flag:
    print(hex(ord(f)), end="")
    i = i + 1
    if(i%4 == 0):
        print('\n')
