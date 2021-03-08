#!/bin/bash

# get to home
cd /home/rooted

#drop into the jail!
fakechroot -e "clearing env ;)" chroot ./jail /bin/zsh -i +m
