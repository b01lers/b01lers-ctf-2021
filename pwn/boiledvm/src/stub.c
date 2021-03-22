
#define _GNU_SOURCE
#include <linux/seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/ptrace.h>
#include <signal.h>
#include <string.h>
#include <pthread.h>
#include <sys/mman.h>
#include <string.h>
#include <sys/ioctl.h>
#include <fcntl.h>


//#define DEBUG



unsigned char hex2bin(unsigned char* hex){
    unsigned char c = *hex;
    unsigned char t=0;
    if (c >= '0' && c <= '9') {
        t += c - '0';
    } else if (c >= 'A' && c <= 'F') {
        t += c - 'A' + 10;
    } else if (c >= 'a' && c <= 'f') {
        t += c - 'a' + 10;
    }
    t = t << 4;
    c = *(hex+1);
    if (c >= '0' && c <= '9') {
        t += c - '0';
    } else if (c >= 'A' && c <= 'F') {
        t += c - 'A' + 10;
    } else if (c >= 'a' && c <= 'f') {
        t += c - 'a' + 10;
    }
    return t;
}


int main(int argc, char** argv) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    #ifndef DEBUG
    ptrace(PTRACE_TRACEME, 0, 0, 0);
    raise(SIGSTOP);
    #endif   

    unsigned long CODE;
    CODE = strtoul(argv[1], NULL, 16);
    //printf("%lx\n", CODE);

    unsigned char* code = (unsigned char*) mmap((void*)(CODE), (0x1000*3), PROT_READ | PROT_WRITE  | PROT_EXEC, MAP_FIXED |MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    unsigned char* buf[0x1000*3];
    unsigned int p = 0;
    unsigned int v = 0;
    //printf("0\n");
    while(v<sizeof(buf)){
        v = read(0, &(buf[p]), sizeof(buf)-p);
        //printf("- %d\n", v);
        if(v<=0){
            break;
        }
        p+=v;
    }


    memcpy((unsigned char*)CODE, buf, 0x1000*3);

    mprotect((void*)(CODE+0x0), 0x1000, PROT_READ | PROT_EXEC);
    mprotect((void*)(CODE+0x1000), 0x1000, PROT_READ);
    mprotect((void*)(CODE+0x2000), 0x1000, PROT_READ  | PROT_WRITE);

    //seccomp-tools asm -f c_source filter1.seccomp
    #ifndef DEBUG
  static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,9,62,0,0,192,32,0,0,0,0,0,0,0,53,0,7,0,0,0,0,64,21,0,5,0,1,0,0,0,21,0,4,0,0,0,0,0,21,0,3,0,60,0,0,0,21,0,2,0,2,0,0,0,21,0,1,0,11,0,0,0,6,0,0,0,0,0,0,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,0,0};
  struct prog {
    unsigned short len;
    unsigned char *filter;
  } rule = {
    .len = sizeof(filter) >> 3,
    .filter = filter
  };
  if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) { perror("prctl(PR_SET_NO_NEW_PRIVS)"); exit(2); }
  if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) { perror("prctl(PR_SET_SECCOMP)"); exit(2); }
    #endif

    ((void(*)())(CODE))();

}

//clang -O2 -Wl,-z,now -pie -fPIE stub.c -o stub
