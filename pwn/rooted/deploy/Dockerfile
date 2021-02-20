# We can build from whatever version
# we want. 20.04 is most typical now.

FROM ubuntu:20.04

# Install any software needed to
# build the challenge
#TODO: finish with software needed

RUN apt-get update && \
    apt-get install -y \
    xinetd \
    fakechroot \
    debootstrap \
    fakeroot \
    zsh

# Change example to the name of your challenge.
ENV USER rooted
WORKDIR /home/$USER
RUN useradd $USER

# This adds the critical files.
##TODO: add chrooting and stuff

# wrapper.sh wraps the executable by 
# `cd`ing to the right place
COPY ./deploy/wrapper.sh /home/$USER/

# The xinetd configuration provides run options
# but is very boilerplate. See below. 
#add in files
COPY ./deploy/$USER.xinetd /etc/xinetd.d/$USER
COPY ./solve/flag.txt /home/$USER/flag.txt

#setup the jail files
# this way not needed with every xinetd connection
#delete file once exeecuted
COPY ./src/setup.sh /home/$USER/setup.sh
RUN /home/$USER/setup.sh
RUN rm /home/$USER/setup.sh

# This runs make in the challenge dir
#RUN make -C /home/$USER/

# Set permissions. Be *VERY* careful
# about changing this!
RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER
RUN chmod -x /home/$USER/flag.txt
RUN touch /var/log/xinetdlog

# Whatever port you configured in xinetd.
# PROBABLY this should stay 1337. Just change
# The passthrough port in docker-compose.yml below.
EXPOSE 1337

# Start the container by starting xinetd and outputting
# the xinetd log for debugging.
#CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
#DEBUGGING: 
CMD /bin/zsh
