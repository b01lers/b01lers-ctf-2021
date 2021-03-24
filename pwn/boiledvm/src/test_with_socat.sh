#!/bin/sh

socat TCP-LISTEN:7777,reuseaddr,fork EXEC:"python ../dist/boiledvm.py" &
P=$!
(
    sleep 1
    cd ../solve
    ./solve.py 127.0.0.1 7777
)
kill -9 $P

