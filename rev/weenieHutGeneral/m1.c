#include <stdio.h>
#include <stdlib.h>
#include "revvy.h"

void tryToRev(int);

void tryToRev(int input)
{
	revvy();
	if((input ^ 0x98c3a78b ^ rand() ^ 0xad5410ca) == rand()) {
		printf("Password Accepted, welcome to weenie hut general! Submit input as flag!\n");
	}
	
	else {
		printf("That's incorrect. Try going to weenie hut junior.\n");
	}
}






