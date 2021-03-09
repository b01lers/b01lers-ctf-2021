FROM ubuntu:18.04

RUN apt-get update
#RUN apt-get install -y xinetd
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask

#RUN touch /var/log/xinetdlog
EXPOSE 5000

# Change example to the name of your challenge.
ENV USER loremipsum

WORKDIR /home/$USER

RUN useradd $USER

#COPY ./deploy/wrapper.sh /home/$USER/
#COPY ./deploy/$USER.xinetd /etc/xinetd.d/$USER
#COPY ./src/$USER.sh /home/$USER/
COPY ./src /home/$USER/
#COPY ./solve/flag.txt /home/$USER/flag.txt

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER

USER loremipsum
CMD python3 loremipsum.py
