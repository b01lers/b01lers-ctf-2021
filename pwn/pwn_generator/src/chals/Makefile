all: chal1 chal1a chal1b chal2 chal2a chal2b chal3 chal3a chal3b

chal1 chal1a chal1b: chal1.c
	gcc chal1.c -o chal1 -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0
	clang chal1.c -o chal1a -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0
	clang chal1.c -o chal1b -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0 -Wl,-z,norelro,-z,execstack

chal2 chal2a chal2b: chal2.c
	gcc chal2.c -o chal2 -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0
	clang chal2.c -o chal2a -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0
	clang chal2.c -o chal2b -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0 -Wl-z,norelro,-z,execstack

chal3 chal3a chal3b: chal3.c
	gcc chal3.c -o chal3 -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0
	clang chal3.c -o chal3a -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0
	clang chal3.c -o chal3b -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0 -Wl-z,norelro,-z,execstack

