from ubuntu:18.04

run apt-get -qq update && apt-get install -qq --no-install-recommends xinetd rsyslog software-properties-common

run add-apt-repository -y ppa:ubuntu-toolchain-r/ppa
run apt-get install -y python3.7
run apt-get install -y python3-pip
run python3.7 -m pip install pip

run apt install -y netcat-traditional htop

#the flag file name must be just "flag"
copy ./solve/flag.txt /flag
copy ./deploy/boiledvm.xinetd /boiledvm.xinetd
copy ./deploy/wrapper.sh /wrapper.sh

copy ./dist/boiledvm.py /boiledvm.py
copy ./src/stub /stub

run chmod o-w /var/tmp
run chmod o-w /dev/shm


expose 4567
#cmd ["sleep", "10000"]
cmd ["/usr/sbin/xinetd", "-syslog", "local0", "-dontfork", "-f", "/boiledvm.xinetd"]

