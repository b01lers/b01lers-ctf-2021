test: main.c librev.so
	gcc -L/home/ndamalas/b01lers/myChal -Wall -o test main.c -lrev

librev.so: m1.o revvy.h
	gcc -shared -o librev.so m1.o revvy.h

m1.o: m1.c
	gcc -c -fpic m1.c