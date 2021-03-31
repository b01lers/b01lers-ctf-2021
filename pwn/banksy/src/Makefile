CC=gcc

chal: chal.c
	$(CC) -o $@ $< -fPIE -pie -fPIC -L$(shell pwd) -Xlinker -rpath=$(shell pwd) -Xlinker -I$(shell pwd) -l:libc.a -l:libpthread.a -l:libdl.a -static -fstack-protector-all -Wl,-z,now,-z,relro -O0
