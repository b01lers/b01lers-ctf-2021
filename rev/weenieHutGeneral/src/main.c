#include <stdio.h>

extern void tryToRev(int);

int main(void)
{
	puts("testing 1...");
	tryToRev(100);
	puts("testing 2...");
	tryToRev(1432175799);
	return 0;
}
