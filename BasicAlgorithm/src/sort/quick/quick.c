#include <stdlib.h>
#include <stdio.h>

void change(int* lst, int ele1_index, int ele2_index) {
    int tmp;
    tmp = lst[ele1_index];
    lst[ele1_index] = lst[ele2_index];
    lst[ele2_index] = tmp;

    return ;
}


typedef struct array
{
    
};


int main()
{
    int arr[5];
    arr[0] = 1;
    arr[1] = 2;

    change(arr, 0, 1);
    printf("%d , %d\n", arr[0], arr[1]);
    return 0;
}