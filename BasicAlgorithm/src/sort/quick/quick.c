#include <stdlib.h>
#include <stdio.h>

void change(int* lst, int ele1_index, int ele2_index) {
    int tmp;
    tmp = lst[ele1_index];
    lst[ele1_index] = lst[ele2_index];
    lst[ele2_index] = tmp;

    return ;
}

int process(int *lst, int low, int high) {
    int pivot_key = lst[low];

    while (low < high){
        while ((low < high) && pivot_key < lst[high]) high --;
        change(lst, high, low);

        while ((low < high) && pivot_key > lst[low]) low ++;
        change(lst, high, low);
    }
    return low;
}

void quick_sort(int *lst, int length) {
    int m;
    m = process(lst, 0, length-1);
    process(lst, 0, m-1);
    process(lst, m+1, length-1);
    return ;
}

void print_array(int *arr, int n, const char *msg) {
    printf("%s: ", msg);
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int arr[] = {5, 2, 8, 3, 9, 1, 7};
    int n = sizeof(arr) / sizeof(arr[0]);

    print_array(arr, n, "Before sorting:");

    quick_sort(arr, n);

    print_array(arr, n, "Sorted:");

    return 0;
}
