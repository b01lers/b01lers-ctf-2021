line = input('>>> ')

blacklist = "()"
for item in blacklist:
    if item in line.lower():
        raise Exception()

exec(line)
