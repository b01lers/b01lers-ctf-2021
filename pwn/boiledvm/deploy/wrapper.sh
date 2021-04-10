#!/bin/sh

timeout -k1 60 stdbuf -i0 -o0 -e0 python3.7 -u /boiledvm.py 2>/dev/null


