#!/usr/bin/env python

import sys

cc = open(sys.argv[1]).read()
if sys.argv[3] == "python":
    sep = "#"
elif sys.argv[3] == "c":
    sep = "//"

out = []
for i, l in enumerate(cc.split("\n")):
    nl = l
    if sep in l and i>0:
        in_single = False
        in_double = False
        for idx, c in enumerate(l):
            if in_single==False and in_double==False:
                if l[idx:idx+len(sep)] == sep:
                    nl = l[:idx]
                    if nl.strip() == "":
                        nl = None
                    break 
                if c == '"':
                    in_double = True
                if c == "'":
                    in_double = True
            elif in_double == True:
                if c == '"':
                    in_double = False
            elif in_single == True:
                if c == "'":
                    in_single = False

    out.append(nl)
outc = "\n".join((l for l in out if l is not None))

with open(sys.argv[2], "w") as fp:
    fp.write(outc)

