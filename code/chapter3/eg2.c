#include <stdio.h> 
#include <stdbool.h>
#define MAX_SIZE 400

typedef bool status;

typedef struct triple {
    int row;
    int column;
    int value;
} triple;

typedef struct sparse_matrix {
    triple data[MAX_SIZE];
    int length, column, row;
} sparse_matrix;

// 定义函数指针类型
typedef status (*transpose_func)(sparse_matrix original_matrix, sparse_matrix* transposed_matrix);

// 示例实现1
status transpose_matrix_implementation1(sparse_matrix original_matrix, sparse_matrix* transposed_matrix) {
    transposed_matrix->column = original_matrix.row;
    transposed_matrix->row = original_matrix.column;
    transposed_matrix->length = original_matrix.length;
    
    for (int i = 0; i < original_matrix.length; i++) {
        transposed_matrix->data[i].row    = original_matrix.data[i].column;
        transposed_matrix->data[i].column = original_matrix.data[i].row;
        transposed_matrix->data[i].value  = original_matrix.data[i].value;
    }
    return true;
}

status transpose_matrix_implementation2(sparse_matrix original_matrix, sparse_matrix* transposed_matrix) { 
    transposed_matrix->column = original_matrix.row;
    transposed_matrix->row = original_matrix.column;
    transposed_matrix->length = original_matrix.length;

    int ele_num = 0;
    
    // 按列扫描（1-based 索引）
    for (int i = 1; i <= original_matrix.column; i++) {
        for (int j = 0; j < original_matrix.length; j++) {
            if (original_matrix.data[j].column == i) {
                transposed_matrix->data[ele_num].row    = i;  // 原来的 column 变成新的 row
                transposed_matrix->data[ele_num].column = original_matrix.data[j].row; // 原来的 row 变成新的 column
                transposed_matrix->data[ele_num].value  = original_matrix.data[j].value;
                ele_num++;
            }
        }
    }
    return true;
}

status transpose_matrix_implementation3(sparse_matrix original_matrix, sparse_matrix* transposed_matrix) { 
    transposed_matrix->column = original_matrix.row;
    transposed_matrix->row = original_matrix.column;
    transposed_matrix->length = original_matrix.length;

    if (original_matrix.length == 0) return true;
    int tmp[original_matrix.column + 1];
    
    for (int i = 1; i <= original_matrix.column; i++) tmp[i] = 0;
    
    for (int i = 0; i < original_matrix.length; i++) {
        int col = original_matrix.data[i].column;
        tmp[col]++;
    }
    
    int cpot[original_matrix.column + 1];
    cpot[1] = 0;  // 第1列从位置0开始（C数组索引）
    for (int col = 2; col <= original_matrix.column; col++) cpot[col] = cpot[col - 1] + tmp[col - 1];
    
    for (int j = 0; j < original_matrix.length; j++) {
        int col = original_matrix.data[j].column;
        int pos = cpot[col];  // 当前列应该放置的位置
        
        transposed_matrix->data[pos].row = original_matrix.data[j].column;
        transposed_matrix->data[pos].column = original_matrix.data[j].row;
        transposed_matrix->data[pos].value = original_matrix.data[j].value;
        
        cpot[col]++;
    }
    
    return true;
}

// ======================== 测试函数 ========================
void test_transpose(transpose_func func, const char* func_name) {
    printf("=== Test for %s ===\n", func_name);
    
    // 测试用例1:普通情况
    printf("\ntest1:3x3\n");
    sparse_matrix m1 = {
        .data = {{1,2,10}, {2,1,20}, {3,3,30}},
        .length = 3, .row = 3, .column = 3
    };
    
    sparse_matrix t1;
    func(m1, &t1);
    
    printf("matrix:");
    for (int i = 0; i < m1.length; i++) {
        printf("(%d,%d,%d) ", m1.data[i].row, m1.data[i].column, m1.data[i].value);
    }
    printf("\ntransposed:");
    for (int i = 0; i < t1.length; i++) {
        printf("(%d,%d,%d) ", t1.data[i].row, t1.data[i].column, t1.data[i].value);
    }
    printf("\nExpected Output:  (2,1,10) (1,2,20) (3,3,30)\n");
    
    printf("verify its dimension:%dx%d -> %dx%d %s\n", 
           m1.row, m1.column, t1.row, t1.column,
           (t1.row == m1.column && t1.column == m1.row) ? "Bingo" : "Error");
    
    // 测试用例2:空矩阵
    printf("\ntest2:empty matrix\n");
    sparse_matrix m2 = { .length = 0, .row = 3, .column = 3 };
    sparse_matrix t2;
    func(m2, &t2);
    printf("transposed length:%d %s\n", t2.length, t2.length == 0 ? "Bingo" : "Error");
    
    // 测试用例3:单元素
    printf("\ntest3:single element\n");
    sparse_matrix m3 = {
        .data = {{2,2,99}},
        .length = 1, .row = 3, .column = 3
    };
    sparse_matrix t3;
    func(m3, &t3);
    printf("single element:(%d,%d,%d) -> (%d,%d,%d) %s\n",
           m3.data[0].row, m3.data[0].column, m3.data[0].value,
           t3.data[0].row, t3.data[0].column, t3.data[0].value,
           (t3.data[0].row == 2 && t3.data[0].column == 2 && t3.data[0].value == 99) ? "Bingo" : "Error");
    
    // 测试用例4:验证数学正确性（转置两次应该恢复）
    printf("\ntest4:Matrix should equal to the result transposed two times\n");
    sparse_matrix m4 = {
        .data = {{1,3,5}, {2,1,7}, {2,2,9}},
        .length = 3, .row = 3, .column = 4
    };
    sparse_matrix t4, t4_again;
    
    func(m4, &t4);
    func(t4, &t4_again);
    
    printf("matrix:");
    for (int i = 0; i < m4.length; i++) {
        printf("(%d,%d,%d) ", m4.data[i].row, m4.data[i].column, m4.data[i].value);
    }
    printf("\ntranspose twice:");
    for (int i = 0; i < t4_again.length; i++) {
        printf("(%d,%d,%d) ", t4_again.data[i].row, t4_again.data[i].column, t4_again.data[i].value);
    }
    
    bool restored = true;
    for (int i = 0; i < m4.length; i++) {
        bool found = false;
        for (int j = 0; j < t4_again.length; j++) {
            if (m4.data[i].row == t4_again.data[j].row &&
                m4.data[i].column == t4_again.data[j].column &&
                m4.data[i].value == t4_again.data[j].value) {
                found = true;
                break;
            }
        }
        if (!found) {
            restored = false;
            break;
        }
    }
    printf("\nrestored:%s\n", restored ? "Bingo" : "Error");
}

// ======================== 辅助函数 ========================
void print_matrix_dense(sparse_matrix m) {
    printf("matrix %dx%d:\n", m.row, m.column);
    int dense[m.row][m.column];
    
    for (int i = 0; i < m.row; i++)
        for (int j = 0; j < m.column; j++)
            dense[i][j] = 0;
    
    for (int k = 0; k < m.length; k++) {
        dense[m.data[k].row-1][m.data[k].column-1] = m.data[k].value;
    }
    
    for (int i = 0; i < m.row; i++) {
        for (int j = 0; j < m.column; j++) {
            printf("%3d", dense[i][j]);
        }
        printf("\n");
    }
}

void test_visual(transpose_func func, const char* func_name) {
    printf("\n=== visualization for %s ===\n", func_name);
    
    sparse_matrix m = {
        .data = {{1,2,5}, {2,1,3}, {3,3,7}},
        .length = 3, .row = 3, .column = 3
    };
    
    sparse_matrix t;
    func(m, &t);
    
    printf("matrix\n");
    print_matrix_dense(m);
    
    printf("\ntransposed:\n");
    print_matrix_dense(t);
    
    printf("\ntriple belike:");
    for (int i = 0; i < t.length; i++) {
        printf("(%d,%d,%d) ", t.data[i].row, t.data[i].column, t.data[i].value);
    }
    printf("\n");
}

// ======================== main ========================
int main() {
    test_transpose(transpose_matrix_implementation1, "transpose_matrix_implementation1");
    test_visual(transpose_matrix_implementation1, "transpose_matrix_implementation1");
    
    test_transpose(transpose_matrix_implementation2, "transpose_matrix_implementation2");
    test_visual(transpose_matrix_implementation2, "transpose_matrix_implementation2");

    test_transpose(transpose_matrix_implementation3, "transpose_matrix_implementation3");
    test_visual(transpose_matrix_implementation3, "transpose_matrix_implementation3");
    
    return 0;
}
