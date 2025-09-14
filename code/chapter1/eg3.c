// chapter1 eg3.c
#include <stdio.h>

int main(void) {
    int start, time, end;
    end = 1024;
    start = 1;
    for (time = 0; start != end; start*=2) time++;
    printf("%d equals to the %d power of 2.\n", end, time);
    return 0;
}