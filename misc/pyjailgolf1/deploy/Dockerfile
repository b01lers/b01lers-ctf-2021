FROM ubuntu:20.10

RUN apt-get update
RUN apt-get install -y xinetd
RUN apt-get install -y python3

RUN touch /var/log/xinetdlog
EXPOSE 1337

# Change example to the name of your challenge.
ENV USER pyjailgolf1

WORKDIR /home/$USER

RUN useradd $USER

COPY ./deploy/wrapper.sh /home/$USER/
COPY ./deploy/$USER.xinetd /etc/xinetd.d/$USER
COPY ./src/$USER.py /home/$USER/

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER

CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
# CMD bash
