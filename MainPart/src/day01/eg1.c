#include <stdio.h>
#include <string.h>

int main() {
    int arr[10];
    memset(arr, 0, sizeof(int) * 4);

    arr[1] = 1;
    *(&arr[0] + 2) = 2;
    printf("%d\n%d\n", arr[1], arr[2]);
    return 0;
}