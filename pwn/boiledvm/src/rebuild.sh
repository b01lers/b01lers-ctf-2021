#!/bin/bash


rm ../dist/boiledvm.py
rm ../dist/stub
rm ../solve/flag.txt

./remove_comments.py boiledvm.py ../dist/boiledvm.py python
rm stub
clang -O2 -Wl,-z,now -pie -fPIE stub.c -o stub
cp stub ../dist/
cp flag ../solve/flag.txt
