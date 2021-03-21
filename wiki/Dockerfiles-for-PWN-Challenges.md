Writing pwn challenges is tricky for a few reasons. Chief among them is that when someone pwns our system we don't actually want them to own it! This is how we set up our dockers.

The technologies:
1. Docker Compose
2. Xinetd
3. Docker Engine

Using these 3 technologies allow us to do the following:
1. Have our challenges automatically start when connected to
2. Sandbox our challenges so users with shell can't destroy the whole challenge box
3. Distribute challenge binaries/libraries built on the docker so there is minimal discrepancy between local and remote
4. Handle many connections concurrently
5. Do everything easily and efficiently

Note that for all of the below I assume the directory structure:

```
-+ example
 +-+ dist
 | +- Dockerfile
 | +- Dockerfile-build
 | +- docker-compose.yml
 | +- example.xinetd
 | +- wrapper.sh
 +-+ src
   +- example.c
   +- example.Makefile 
```

There are other things that need to be in a directory to distribute a challenge but this is the minimum for *deployment*.

How do we set this up? First, a dockerfile.

```
# We can build from whatever version
# we want. 20.04 is most typical now.

# FROM ubuntu:18.04
FROM ubuntu:20.04

# Install any software needed to
# build the challenge

RUN apt-get update
RUN apt-get install -y xinetd
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y gcc-multilib

# Change example to the name of your challenge.

ENV USER example
WORKDIR /home/$USER
RUN useradd $USER

# This adds the critical files.

# wrapper.sh wraps the executable by 
# `cd`ing to the right place

COPY ./deploy/wrapper.sh /home/$USER/

# The xinetd configuration provides run options
# but is very boilerplate. See below. 
COPY ./deploy/$USER.xinetd /etc/xinetd.d/$USER

# This assumes a C file but works perfectly OK
# with go/C++/rust, just install the right compiler
COPY ./src/$USER.c /home/$USER/

# This makefile provides the build and outputs
# the challenge binary (see below)
COPY ./src/$USER.Makefile /home/$USER/Makefile

# We don't want to forget the flag!
COPY ./solve/flag.txt /home/$USER/flag.txt

# This runs make in the challenge dir
RUN make -C /home/$USER/

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
CMD service xinetd start && sleep 2 && tail -f /var/log/xinetdlog
```

To go along with this template dockerfile, we typically use a docker-compose file:

```
version: "3.7"
services:
    example:
        container_name: example
        build:
            dockerfile: ./deploy/Dockerfile
            context: ../
        logging:
            driver: "json-file"
        ports:
            - "6666:1337"
    example-build:
        container_name: example-build
        build:
            dockerfile: ./deploy/Dockerfile-build
            context: ../
        logging:
            driver: "json-file"
        volumes:
            - build:/home/example/build
volumes:
    build:
        name: example-build
        driver: local
        driver_opts:
            type: none
            device: /home/b01lers/some-path-to-output-the-binary
            o: bind
```

The only things we have to change here are the name, `example`, and the device path. This docker-compose file will start two containers, one to actually run the program with xinetd, another to just build it in the same environment and exit. This is important because building it on your own machine may not be exactly the same as building on the docker!

The device path is where the container will output the built challenge binary.

Now, we also need a build dockerfile. This looks like the below, typically:

```
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y gcc-multilib

# Change example to the name of your challenge.
# Set up the user
ENV USER example
WORKDIR /home/$USER
RUN useradd $USER

# Add source files
COPY ./src/$USER.c /home/$USER/
COPY ./src/$USER.Makefile /home/$USER/Makefile

# Copy the binary AND any libraries it depends on
# into the build output directory
RUN mkdir /home/$USER/build
RUN make -C /home/$USER/ && cp /home/$USER/$USER /home/$USER/build/$USER && sh -c "ldd /home/$USER/build/$USER | grep '=>' | cut -d' ' -f3 | xargs -I '{}' cp -L -v '{}' /home/$USER/build/"

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER

CMD sleep 5
```

The final pieces of the puzzle are the wrapper and xinetd configuration. The xinetd configuration:

```
service metacortex
{
        disable                 = no
        socket_type             = stream
        protocol                = tcp
        wait                    = no
        log_type                = FILE /var/log/xinetdlog
        log_on_success          = HOST PID EXIT DURATION
        log_on_failure          = HOST

        # Change the username to the name of your challenge
        user                    = example

        bind                    = 0.0.0.0

        # Change the server to your executable
        server                  = /home/example/wrapper.sh

        type                    = UNLISTED

        # Change the PORT to your desired challenge port
        port                    = 1337

        per_source              = 10
}
```

This provides ratelimiting (again, change `example` to the challenge name) and super serving the challenge. Finally, the wrapper:

```sh
#!/bin/bash
cd /home/example/ && ./example
```

What this does is every time xinetd accepts a connection on port 1337, it will run the script (which does a `cd` and runs the challenge) as if its stdin and stdout were the socket. It abstracts and simplifies the entire process significantly.