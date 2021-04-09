FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask

EXPOSE 5000

# Change example to the name of your challenge.
ENV USER loremipsum

WORKDIR /home/$USER

RUN useradd $USER

COPY ./src /home/$USER/

RUN chown -R root:$USER /home/$USER
RUN chmod -R 550 /home/$USER

RUN sed -i 's/self._failed_pin_auth += 1/self._failed_pin_auth += 0/g' /usr/local/lib/python3.6/dist-packages/werkzeug/debug/__init__.py

USER loremipsum
CMD python3 loremipsum.py
