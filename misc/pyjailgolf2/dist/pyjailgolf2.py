line = input('>>> ')

flag="[REDACTED]"

if len(line) > 9:
    raise Exception()

try:
    eval(line)
except:
    pass
