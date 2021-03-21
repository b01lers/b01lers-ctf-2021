#include<stdlib.h>
#include<stdio.h>
#include<unistd.h>
#include<string.h>

#define DEBUG 0

#define NUM_CHUNKS 4
#define MIN_SIZE 0xff000
#define MAX_SIZE 2147483647

#if DEBUG
    #define CHECK_IDX(idx) if(idx > NUM_CHUNKS - 1 || idx < 0) { printf("Invalid idx.\n"); return 0;}
    #define CHECK_SIZE(size) if(size > MAX_SIZE || size < MIN_SIZE) { printf("Invalid size.\n"); return 0;}
    #define CHECK_OFFSET(idx, offset) if(offset > chunks[idx].size) { printf("Invalid offset.\n"); return 0;}
#else
    #define CHECK_IDX(idx) if(idx > NUM_CHUNKS - 1 || idx < 0) { return 0; }
    #define CHECK_SIZE(size) if(size > MAX_SIZE || size < MIN_SIZE) { return 0; }
    #define CHECK_OFFSET(idx, offset) if(offset > chunks[idx].size) { return 0; }
#endif

typedef struct {
    char * ptr;
    long size;
} chunk;

chunk chunks[NUM_CHUNKS];

int my_alloc(int idx, long size) {
    CHECK_SIZE(size);
    CHECK_IDX(idx);
    chunks[idx].ptr = malloc(size);
    chunks[idx].size = size;
}

int my_free(int idx) {
    CHECK_IDX(idx);
    free(chunks[idx].ptr);
    memset(&chunks[idx], '\0', sizeof(chunk));
}

int my_read(int idx, long offset) {
    CHECK_IDX(idx);
    CHECK_OFFSET(idx, offset);

    read(0, chunks[idx].ptr + offset, 32);
}

int main() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    int choice;
    int idx;
    long size;
    int n_matched;
    int count = 0;

    while(1) {
        if(feof(stdin) || count >= 30) {
            exit(0);
        }
        printf("1: alloc; 2: free; 3: write> ");
        n_matched = scanf("%d", &choice);
        if(!choice || !n_matched) {
            break;
        }

        if(choice == 1) {
            count += 1;

            printf("idx> ");
            n_matched = scanf("%d", &idx);
            printf("size> ");
            n_matched = scanf("%ld", &size);

            my_alloc(idx, size);
        }

        if(choice == 2) {
            count += 5;

            printf("idx> ");
            n_matched = scanf("%d", &idx);

            my_free(idx);
        }
        if(choice == 3) {
            count += 3;
            printf("idx> ");
            n_matched = scanf("%d", &idx);
            printf("offset> ");
            n_matched = scanf("%ld", &size);

            my_read(idx, size);
        }
    }
}
