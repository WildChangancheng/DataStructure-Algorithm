#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int start;
    int end;
    int capacity;
    int real_size;
    int *content;
} MyCircularDeque;

MyCircularDeque* myCircularDequeCreate(int k) {
    MyCircularDeque* obj = calloc(1, sizeof(MyCircularDeque));
    obj->capacity = k;
    obj->start = 0;
    obj->end = 0;
    obj->real_size = 0;
    obj->content = calloc(k, sizeof(int));
    return obj;
}

// 判断是否可以插入（未满）
bool is_valid_to_insert(MyCircularDeque* obj) {
    return obj->real_size < obj->capacity;
}

// 计算循环位置
int get_position(int pos, int capacity, int move) {
    return (pos + move + capacity) % capacity;
}

bool myCircularDequeInsertFront(MyCircularDeque* obj, int value) {
    if (!is_valid_to_insert(obj)) return false;
    obj->start = get_position(obj->start, obj->capacity, -1);
    obj->content[obj->start] = value;
    obj->real_size++;
    return true;
}

bool myCircularDequeInsertLast(MyCircularDeque* obj, int value) {
    if (!is_valid_to_insert(obj)) return false;
    obj->content[obj->end] = value;
    obj->end = get_position(obj->end, obj->capacity, +1);
    obj->real_size++;
    return true;
}

bool myCircularDequeDeleteFront(MyCircularDeque* obj) {
    if (obj->real_size == 0) return false;
    obj->start = get_position(obj->start, obj->capacity, +1);
    obj->real_size--;
    return true;
}

bool myCircularDequeDeleteLast(MyCircularDeque* obj) {
    if (obj->real_size == 0) return false;
    obj->end = get_position(obj->end, obj->capacity, -1);
    obj->real_size--;
    return true;
}

int myCircularDequeGetFront(MyCircularDeque* obj) {
    if (obj->real_size == 0) return -1;
    return obj->content[obj->start];
}

int myCircularDequeGetRear(MyCircularDeque* obj) {
    if (obj->real_size == 0) return -1;
    int rear_index = get_position(obj->end, obj->capacity, -1);
    return obj->content[rear_index];
}

bool myCircularDequeIsEmpty(MyCircularDeque* obj) {
    return (obj->real_size == 0);
}

bool myCircularDequeIsFull(MyCircularDeque* obj) {
    return (obj->real_size == obj->capacity);
}

void myCircularDequeFree(MyCircularDeque* obj) {
    free(obj->content);
    free(obj);
}


/**
 * Your MyCircularDeque struct will be instantiated and called as such:
 * MyCircularDeque* obj = myCircularDequeCreate(k);
 * bool param_1 = myCircularDequeInsertFront(obj, value);
 
 * bool param_2 = myCircularDequeInsertLast(obj, value);
 
 * bool param_3 = myCircularDequeDeleteFront(obj);
 
 * bool param_4 = myCircularDequeDeleteLast(obj);
 
 * int param_5 = myCircularDequeGetFront(obj);
 
 * int param_6 = myCircularDequeGetRear(obj);
 
 * bool param_7 = myCircularDequeIsEmpty(obj);
 
 * bool param_8 = myCircularDequeIsFull(obj);
 
 * myCircularDequeFree(obj);
*/