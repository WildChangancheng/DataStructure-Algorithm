#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int length;
    int max_length;
    int *content;
    // 注意，这里的content只是一个int *指针
    // 而不是一整个数组，所以实际上只是一个8bit的pointer罢了
} Array;

Array* array_create(int max_length) {
    if (max_length<0) {
        printf("Invalid max_length is given.\n");
        exit(-1);
    }
    Array* arr = (Array*)malloc(sizeof(Array));
    arr->length = 0;
    arr->max_length = max_length;
    arr->content = (int*)calloc(max_length, sizeof(int));
    // 注意，.是用在结构体本身的
    // ->是用在结构体的指针上的，先解引用，实际上是个语法糖
    // otherwise, content是指针
    return arr;
}

bool is_valid_index(const Array* arr, int index) {
    return (index >= 0 && index < arr->max_length);
}

void array_show(const Array* arr) {
    printf("[");
    for (int i = 0; i < arr->length; i++) {
        printf("%d", arr->content[i]);
        if (i < arr->length - 1) printf(", ");
    }
    printf("]\n");
}

int array_read(const Array* arr, int index) {
    if (!is_valid_index(arr, index)) exit(-1);
    if (index>=arr->length) exit(-1);
    return arr->content[index];
}

void array_insert(Array* arr, int index, int value) {
    if (!is_valid_index(arr, index)) return ;
    if (index > arr->length) return;
    if (index == arr->length) {
        arr->content[index] = value;
        arr->length++;
        return ;
    }
    for (int i = arr->max_length; i>index; i--) arr->content[i] = arr->content[i-1];
    arr->content[index] = value;
    arr->length++;
}

void array_delete(Array* arr, int index) {
    if (!is_valid_index(arr, index)) return;
    if (index >= arr->length) return;
    if (index == arr->length - 1) {
        arr->length--;
        return;
    }
    
    for (int i = index; i < arr->length - 1; i++) arr->content[i] = arr->content[i + 1];
    arr->length--;
}

void array_update(Array* arr, int index, int new_value) {
    array_delete(arr, index);
    array_insert(arr, index, new_value);
}

int main(void) {
    int n;
    printf("Type in how many elements you'd like to store:");
    scanf("%d", &n);
    printf("\nYou typed in %d. \n", n);
    // input
    
    Array* arr = array_create(n);
    printf("Array is created\n");

    array_show(arr);
    // 可以看到一个空array

    array_insert(arr, 0, 2);
    array_insert(arr, 0, 1);
    array_insert(arr, 0, 0);
    array_show(arr); // [0, 1, 2]
    
    array_insert(arr, 3, 4);
    array_insert(arr, 3, 3);
    array_show(arr); // [0, 1, 2, 3, 4]
    
    // 测试读取操作
    printf("Element at index 3: %d\n", array_read(arr, 3)); // 3
    
    // 测试删除操作
    array_delete(arr, 3);
    array_show(arr); // [0, 1, 2, 4]
    
    // 测试更新操作
    array_update(arr, 3, 5);
    array_show(arr); // [0, 1, 2, 5]
    
    return 0;
}
