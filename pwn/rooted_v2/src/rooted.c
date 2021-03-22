#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>

#define BUFSIZE 250

void opt_a(char * buf){

  //print out buffer
  puts("PRINTING!");
  printf("%s\n",buf);

  //setup assembly for the function
  //  ;write
  //  mov rax, 0x1 ;pop 0x1 (write)
  //  mov rdi, 2 ;setup stdout 1
  //  mov rbx, 0x000a6e696d646169
  //  push rbx
  //  mov rsi, rsp ;give pointer to char *
  //  mov rdx, 0x8
  //  syscall
  //  ;exit smooth transition
  //  add rsp,0x32
  //  xor rdi,rdi ;error_code = 0
  //  push 0x3c ;sys_exit 60
  //  pop rax
  //  syscall ;clear rax and fill with 1 for exit
  //char * admin_shell = "\xb8\x01\x00\x00\x00\xbf\x02\x00\x00\x00\x48\xbb\x69\x61\x64\x6d\x69\x6e\x0a\x00\x53\x48\x89\xe6\xba\x08\x00\x00\x00\x0f\x05\x48\x83\xc4\x32\x48\x31\xff\x6a\x3c\x58\x0f\x05";
}
void opt_b(char * buf){
  //zao gao!!!
  puts("糟糕!");
  ((void (*)())buf)();
}

int main(int argc, char **argv){

  //setup buffer so its nice over nc
  setvbuf(stdout, NULL, _IONBF, 0);

  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  //setup vars
	char op = 'B'; //THE GOAL
  char * ptr = mmap((void*)0,BUFSIZE,PROT_EXEC|PROT_WRITE,MAP_ANONYMOUS|MAP_PRIVATE,-1,0);

	//take input
  puts("HI ADMIN :) YOUR CODE IS SETUP, WHAT DO YOU WANT ME TO PRINT?");
	fgets(ptr, BUFSIZE, stdin);
	
	//make sure we have 'A' as the opcode!
  int len1 = strlen(ptr);
	if(len1 > 6){
		op = 'A';	
	}
  
  //for loop
  for( int i = 0; i < len1; i++){

    //Do something to make it B
    op = ptr[i]^'X';
    
    //switch
    switch(op){
      case 'A':
        break;
      case 'B':
        break;
      default:
        op = 'A';
        break;
    }

    //bad if state
		if (op == 'A'){
			opt_a(ptr);
		} else if(op == 'B'){
      //vulnerable function call of ptr
			opt_b(ptr);
		}
  }

  return 0;
}

