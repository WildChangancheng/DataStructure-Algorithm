#include <stdlib.h>


typedef struct {
    int* content;
    int* sum_array;
    int numsize;
} NumArray;


NumArray* numArrayCreate(int* nums, int numsSize) {
    // NumArray* num_array;
    // 这是不对的，因为这样是野指针
    NumArray* num_array = (NumArray *) calloc(1, sizeof(NumArray));

    num_array -> content = (int *) calloc(numsSize, sizeof(int));
    num_array -> sum_array = (int *) calloc(numsSize+1, sizeof(int));
    num_array -> numsize = numsSize;
    int tmp = 0;

    for (int i = 0; i < numsSize; i++) {
        num_array -> content [i] = nums [i];
        tmp += nums[i];
        num_array -> sum_array[i+1] = tmp;
    }
    return num_array;
}

int numArraySumRange(NumArray* obj, int left, int right) {
    return (obj->sum_array[right+1] - obj->sum_array[left]);
}

void numArrayFree(NumArray* obj) {
    free(obj -> content);
    free(obj -> sum_array);
    free(obj);
    return ;
}

/**
 * Your NumArray struct will be instantiated and called as such:
 * NumArray* obj = numArrayCreate(nums, numsSize);
 * int param_1 = numArraySumRange(obj, left, right);
 
 * numArrayFree(obj);
*/