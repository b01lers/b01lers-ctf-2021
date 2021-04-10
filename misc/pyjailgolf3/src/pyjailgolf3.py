from collections.abc import __builtins__

bi = __builtins__
del bi["help"]

line = input(">>> ")

flag = "pctf{Un1c0d3_i5_sw34t_2}"

if len(line) > 10:
    raise Exception()

try:
    eval(line, {"__builtins__": bi}, locals())
except:
    pass
