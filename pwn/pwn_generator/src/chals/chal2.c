#include<stdio.h>

int main() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    // break up main in random line increments into seperate functions
    char input[48]; // buffer varies
    puts("Name: "); // puts, printf, write, fwrite. print_output function, Text varies
    gets(input); // gets, fgets, scanf, strcpy, memcpy, fread
    puts("Hello, "); // puts, printf, write, fwrite print_output function text varies
    puts(input);
}
