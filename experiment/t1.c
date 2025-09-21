#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int length;
    scanf("%d", &length);
    int *even_number = calloc(length, sizeof(int));
    int *odd_number = calloc(length, sizeof(int));
    int *result = calloc(length, sizeof(int));
    int *final = calloc(length, sizeof(int));
    int min;
    int even_index = 0;
    int odd_index = 0;
    int result_index = 0;
    int fina_index = 0;
    // Apply for memory

    for (int i = 0; i < length; i++) {
        int input;
        scanf("%d", &input);
        if (!(input%2)) {
            even_number[even_index] = input;
            even_index++;
        } else {
            // includes case of result equals to 1 and -1
            odd_number[odd_index] = input;
            odd_index++;
        }
    }
    // Input and storage

    // test part
    // printf("p1\n");
    // for (int i = 0; i<even_index; i++) printf("%d\n", even_number[i]);
    // printf("p2\n");
    // for (int i = 0; i<odd_index; i++) printf("%d\n", odd_number[i]);
    min = (even_index>odd_index)?odd_index:even_index;
    for (int i = 0; i<=min; i+=1, result_index+=2) {
        result[result_index] = even_number[i];
        result[result_index+1] = odd_number[i];
    }

    // test part
    // for (int i = 0; i < length; i++) {
    //     printf("--%d\n", result[i]);
    // }

    result_index -= 2;
    // printf("%d, %d, %d\n", result_index, odd_index, even_index);

    if (even_index>min) {
        for (int i = min; i<=even_index; i++, result_index++) result[result_index] = even_number[i];
    } else {
        for (int i = min; i<=odd_index; i++, result_index++) result[result_index] = odd_number[i];
    }
    // merge part

    // test part
    // for (int i = 0; i < length; i++) {
    //     printf("%d\n", result[i]);
    // }

    int pre=result[0];
    result_index = 0;

    for (; result_index < length;) {
        if(result_index==0) {
            final[fina_index] = result[result_index];
            result_index++;
            fina_index++;
        } else {
            if (result[result_index] != pre) {
                pre = result[result_index];
                final[fina_index] = result[result_index];
                result_index ++;
                fina_index ++;
            } else {
                result_index++;
            }
        }
    }

    for (int i = 0; i < fina_index; i ++ ) {
        printf("%d ", final[i]);
    }


    return 0;

}