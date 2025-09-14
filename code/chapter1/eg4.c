// chapter1 eg4.c
#include <stdio.h>

int main() {
    int n;
    printf("Type in number n: ");
    scanf("%d", &n);

    int count = 0;

    // 双重循环，时间复杂度 O(n^2)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            count++;
        }
    }

    printf("Total operation time: %d\n", count);
    return 0;
}