line = input('>>> ')

flag="[REDACTED]"

if len(line) > 10:
    raise Exception()

try:
    eval(line)
except:
    pass
