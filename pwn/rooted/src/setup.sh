#!/bin/bash
#setup directories
cd /home/rooted/
mkdir ./jail
mkdir ./jail/lib
mkdir ./jail/lib/x86_64-linux-gnu
mkdir ./jail/lib64/
mkdir ./jail/bin
mkdir ./jail/etc
mkdir -p ./jail/usr/lib/x86_64-linux-gnu/zsh/5.8/zsh/

#setup shared objects
ldd /bin/zsh | awk '{print $3}' | xargs -I {} -exec cp {} ./jail/lib/x86_64-linux-gnu/
cp /lib64/ld-linux-x86-64.so.2 ./jail/lib64/
cp /usr/lib/x86_64-linux-gnu/zsh/5.8/zsh/*.so ./jail/usr/lib/x86_64-linux-gnu/zsh/5.8/zsh/

#copy binaries
cp /bin/zsh ./jail/bin/
