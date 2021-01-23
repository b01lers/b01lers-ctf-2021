FROM i386/ubuntu:latest

RUN apt-get -y update
RUN apt-get -y install xinetd

ENV USER banksy
WORKDIR /home/$USER
RUN useradd $USER

COPY ./deploy/wrapper.sh /home/$USER
COPY ./deploy/$USER.xinetd /etc/xinetd.d/$USER
COPY ./dist/$USER /home/$USER/$USER
COPY ./solve/flag.txt /home/$USER/flag.txt

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER
RUN chmod -x /home/$USER/flag.txt
RUN touch /var/log/xinetdlog

EXPOSE 1337

CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
