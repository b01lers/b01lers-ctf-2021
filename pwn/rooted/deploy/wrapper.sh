#!/bin/bash

# get to home
cd /home/rooted

#drop into the jail!
fakechroot -e "export PS1='>'" chroot ./jail /bin/zsh -i +m
