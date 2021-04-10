FROM ubuntu:20.10

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y xinetd 
RUN apt-get install -y clang

RUN touch /var/log/xinetdlog
EXPOSE 1337

# Change example to the name of your challenge.
ENV USER middleagedheap

WORKDIR /home/$USER

RUN useradd $USER

COPY ./deploy/wrapper.sh /home/$USER/
COPY ./deploy/$USER.xinetd /etc/xinetd.d/$USER
COPY ./src/$USER.c /home/$USER/
COPY ./src/Makefile /home/$USER/Makefile
COPY ./solve/flag.txt /home/$USER/flag.txt

RUN make -C /home/$USER/

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER
RUN chmod -x /home/$USER/flag.txt

CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
# CMD bash
