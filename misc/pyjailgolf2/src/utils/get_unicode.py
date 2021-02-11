import unicodedata
good = []
all_unicode = map(chr, range(0x110000))
for c in all_unicode:
    category = unicodedata.category(c)
    if c.isidentifier():
        try:
            # print('    OK [{}] {} U+{:04X}  {}'.format(category, c, ord(c), unicodedata.name(c)))
            normalized = unicodedata.normalize('NFKC', c)
            if len(normalized) > 1 and all(ord(c) < 128 for c in normalized):
                good.append([c, normalized])
        except:
            pass

print(good)

