docker run --privileged --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --security-opt apparmor=unconfined -it -v $(pwd):/opt/src/ vfprintf-chal:latest bash
