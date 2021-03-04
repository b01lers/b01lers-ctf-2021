#!/bin/bash
#setup directories
cd /home/rooted/
mkdir ./jail
mkdir ./jail/lib
mkdir ./jail/lib/x86_64-linux-gnu
mkdir ./jail/lib64/
mkdir ./jail/bin
mkdir ./jail/etc

#setup shared objects
ldd /bin/zsh | awk '{print $3}' | xargs -I {} -exec cp {} ./jail/lib/x86_64-linux-gnu/
cp /lib64/ld-linux-x86-64.so.2 ./jail/lib64/

#copy binaries
cp /bin/zsh ./jail/bin/

# make secret admin check binary
SECRET=./jail/bin/.admin_check
echo -e "#!/bin/zsh\necho \"YOU'RE NOT ADMIN!\"" > $SECRET
chmod +wx $SECRET
chown rooted:rooted $SECRET

