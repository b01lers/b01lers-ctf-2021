from i386/ubuntu:latest

RUN echo hi
RUN apt -y update
RUN apt -y install build-essential bash vim gdb git software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt -y update
RUN apt -y install gcc-10
RUN git clone https://github.com/longld/peda.git ~/peda && \
    echo "source ~/peda/peda.py" >> ~/.gdbinit
