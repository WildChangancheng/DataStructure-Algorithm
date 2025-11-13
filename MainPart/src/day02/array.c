#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef struct arr
{
    int *content;
    int size;
    // 已用容量
    int capacity;
    // 理论容量
} arr;

arr* create_arr(int capacity) {
    arr *array = (arr*) malloc(sizeof(arr));  // 分配结构体本身
    array->size = 0;
    array->capacity = capacity;
    array->content = (int*) calloc(capacity, sizeof(int));  // 分配元素空间
    // 这里要注意，不可以前面都写array，结果后面返回对array取址
    // 因为那样的话array就是临时变量，等函数执行完就销毁了
    return array;
}

arr* resize(arr* array, int new_size) {
    arr* new_array = create_arr(new_size);

    for (int i = 0; i < array->size; i++) new_array->content[i] = array->content[i];
    new_array -> size = array -> size;

    free(array->content);
    free(array);

    return new_array;
}


bool is_element_index(arr* array, int index) {
    return (0 <= index)  && (index < array->size);
}

bool is_position_index(arr* array, int index) {
    return (0 <= index)  && (index <= array->size);
}

int get_size(arr* array) {
    return array->size;
}

void show_array(arr* array) {
    printf("****************************\n");
    printf("Size: %d | Capacity: %d\n", array -> size, array -> capacity);
    for (int i = 0; i < array-> size; i++) printf("number%2d -%2d ;\n", i+1, array->content[i]);
    return ;
}


arr* append(arr* array, int element) {
    if (array->size == array->capacity) array = resize(array, 2 * array->capacity);
    array -> content[array -> size] = element;
    array -> size ++;
    return array;
}

arr* add(arr* array, int index, int element){
    if (!is_position_index(array, index)) return array;

    if (array->size == array->capacity) array = resize(array, 2 * array->capacity);

    if (index < array->size) {
        for (int j = array -> size; j > index; j-- ) {
            array -> content [j] = array -> content [j-1];
        } 
        array -> content[index] = element;
        array->size++;
    } else if (index == array->size) {
        array = append(array, element);
    } else {
        return array;
    }


    return array;
}

arr* pop(arr* array) {
    array->size --;
    if (array->size<(array->capacity/4)) array = resize(array, array->capacity/2);
    array->content[array->size-1] = 0;
    return array;
}

arr* remove_index(arr* array, int index) {
    if (!is_position_index(array, index)) return array;
    if (array->size<(array->capacity/4)) array = resize(array, array->capacity/2);

    if (index < array->size) {
        for (int j = index; j < array -> size-1; j++ ) {
            array -> content [j] = array -> content [j+1];
        } 
        array -> content[array->size] = 0;
        array->size--;
    } else if (index == array->size) {
        array = pop(array);
    } else {
        return array;
    }

    return array;
}

int main() {
    arr *array = create_arr(5);

    for (int i = 0; i < 10; i++) {
        array = append(array, i);
    }

    show_array(array);
    
    array = add(array, 2, 666);
    array = add(array, 11, 666);
    show_array(array);

    array = pop(array);
    show_array(array);

    array = remove_index(array, 2);
    show_array(array);
    return 0;
}