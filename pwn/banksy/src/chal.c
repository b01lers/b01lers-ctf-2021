#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <execinfo.h>
#include <link.h>
#include <pthread.h>
#include <sched.h>
#include <signal.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <wait.h>

#include <sys/mman.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/user.h>

// #define PAGE_SIZE (sysconf(_SC_PAGESIZE))
#define PAGE_ROUND_DOWN(x) (((uint32_t)(x)) & (~(PAGE_SIZE-1)))
#define PAGE_ROUND_UP(x) ( (((uint32_t)(x)) + PAGE_SIZE-1)  & (~(PAGE_SIZE-1)) ) 
#define MEGABYTES(x) ( (1024 * 1024 * x) )
#define M_OFFSETOF(STRUCT, ELEMENT) (unsigned int) &((STRUCT *)NULL)->ELEMENT;
#define D_LINUXNONUSRCONTEXT 0x40000000

extern int __vfprintf_internal (FILE *fp, const char *format, va_list ap, 
        unsigned int mode_flags);

typedef struct targ {
    char buf[0x30];
    void * addr;
    int size;
    void * printf_positional_addr;
    pid_t pid;
} targ;

/*
static void * pf_positional = (void *) 0xcafebabe;
static void * pf_positional_end = (void *) 0xcafebabe;
static void * __vfprintf_internal_printf_positional_offset = (void *) 0x2930;
// static void * printf_positional_size = (void *) 0x00003c9;
static void * _itoa_word_sz = (void *) 0xa0;
static void * __vfprintf_internal_itoa_word_offset = (void *) 0x384b0;
static void * stop_loc = (void *) 0xcafebabe;
*/

int exploit_me(void * userdata) {
    char * buf = (char *) userdata;

    if(raise(SIGSTOP) != 0x00) {
        fprintf(stdout, "raise: %s\n", strerror(errno));
    }

    /* Inputs to solve */
    // AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    // 0
    // %2$.2147483616$p

    /* Trigger printf vulnerability */
    FILE * dn = fopen("/dev/null", "w");
    fprintf(dn, buf);
    fclose(dn);
}

int main() {
    /* Set vbufs for IO */
    setvbuf(stdout, NULL, 0x2, 0x0);
    setvbuf(stdin, NULL, 0x2, 0x0);

    // TODO: rename these
    /*
    stop_loc = (void *)((uint32_t) __vfprintf_internal + (uint32_t) __vfprintf_internal_itoa_word_offset + (uint32_t) _itoa_word_sz);
    fprintf(stdout, "%p\n", stop_loc);
    pf_positional_end = (void *) (((uint32_t) __vfprintf_internal - (uint32_t) __vfprintf_internal_itoa_word_offset) + (uint32_t) _itoa_word_sz);
    pf_positional = (void *) ((uint32_t) __vfprintf_internal - (uint32_t) __vfprintf_internal_itoa_word_offset);
    */


    /* Probablistic, this covers the most common ESP
     * values after corruption */
    uint32_t addr = PAGE_ROUND_UP(0x7f900000);

    /* mmap 0x1000 pages of memor to probablistically
     * de-segfault the stack pivot in printf_positional */
    void * mapping = NULL;
    if ((mapping = mmap((void *) addr, 0x1000 * PAGE_SIZE, PROT_READ | PROT_WRITE, 
                    /* MAP_FIXED | */ MAP_ANONYMOUS | MAP_SHARED, -1, 0x0)) == (void *) -1) {
        fprintf(stdout, "mmap: %s\n", strerror(errno));
    }

    printf("Welcome to graffiti simulator! We have a pretty big\n"
            "wall here....tell me what I should cover it with.\n");

    /* Allow user to put in some ROP goodness */
    char chain_buf[0x30] = {0};
    printf("> ");
    fread(chain_buf, 0x1, 0x30, stdin);
    getchar();

    printf("Oh....well this wall is covered. What wall should we go to?\n");
    printf("> ");
    void * wall_loc;
    fscanf(stdin, "%p", &wall_loc);
    getchar();

    /* This is the actual exploit. TODO: Filter for %n
     * because we don't want to allow blind printf overwrites */
    char exploit_buf[0x12] = {0};
    printf("> ");
    fgets(exploit_buf, 0x11, stdin);
    exploit_buf[0x11] = 0;

    for (char * bb = exploit_buf; bb < (exploit_buf + sizeof(exploit_buf)); bb++) {
        if (*bb == 'n') {
            _exit(1);
        }
    }

    /* Set up the thread argument */
    void * page_addr = (void *) 0x7f900000;

    /* Start a thread of spray_graffiti that overwrites the
     * mapped region with the user-controlled data repeatedly */

    /* TODO: Lower probability but increase frequency ? */
    pid_t tid;
    tid = fork();
    if (tid == -1) {
        fprintf(stdout, "fork: %s\n", strerror(errno));
        _exit(1);
    } else if (tid == 0) {
        exploit_me(exploit_buf);
    } else {


        int status;
        int res;
        int signo = 0;
        int ip;
        int sp;
        int ipoffs;
        int spoffs;
        struct user_regs_struct regs;

        if (ptrace(PTRACE_ATTACH, tid, 0, 0) != 0) {
            fprintf(stdout, "ptrace (PTRACE_ATTACH): %s\n", strerror(errno));
        }

        res = waitpid(tid, &status, WUNTRACED);
        if (res < 0 || !WIFSTOPPED(status) || WSTOPSIG(status) != SIGSTOP) {
            fprintf(stdout, "waitpid: unexpected status %x\n", status);
        }

        status = 0;

        /* We have attach successfully....go go go! */
        while (1) {
            if ((res = ptrace(PTRACE_SINGLESTEP, tid, 0, signo)) < 0) {
                fprintf(stdout, "ptrace (PTRACE_SINGLESTEP): %s\n", strerror(errno));
                _exit(1);
            }

            res = wait(&status);

            if ((signo = WSTOPSIG(status)) == SIGTRAP) {
                signo = 0;
            }

            if ((signo == SIGHUP) || (signo == SIGINT)) {
                ptrace(PTRACE_CONT, tid, 0, signo);
                fprintf(stdout, "ptrace: child exited.\n");
                break;
            }

            if ((res = ptrace(PTRACE_GETREGS, tid, 0, &regs)) != 0) {
                fprintf(stdout, "ptrace (PTRACE_GETREGS): %s\n", strerror(errno));
                _exit(1);
            } else {
                // fprintf(stdout, "%p\n", regs.eip);
                // if (regs.eip == (uint32_t) stop_loc) {
                if (regs.eip == (uint32_t) wall_loc) {
                    for (void * cur = page_addr; cur < page_addr + (0x999 * PAGE_SIZE); cur += sizeof(chain_buf)) {
                        memcpy(cur, chain_buf, sizeof(chain_buf));
                    }
                }
            }
        }

        if (ptrace(PTRACE_CONT, tid, 0, 0) != 0) {
            fprintf(stdout, "ptrace (PTRACE_CONT): %s\n", strerror(errno));
        }
    }
    _exit(0);
}
