#include <stdio.h>
#define MAX_ARRAY_DIM 8




typedef struct array
{
    int *base; // 数组元素基址
    int dim; // 数组实际维数
    int *bounds; // 数组维界地址
    int *constants; // 数组映像函数常量基址
} array;


int main() {
    return 0;
}