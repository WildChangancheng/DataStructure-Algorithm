#include <stdio.h>
#include <conio.h>

typedef struct node
{
    struct node* left, *right;
    int value;
} node;


void create_tree_from_string() {
    return ;
}


int main()
{
    char s[100];
    char ch;
    int index = 0;

    while ((ch = getch()) !='\n') {
        if (ch == ' ') continue;
        s[index] = ch;
        index ++;
    }

    for (int i = 0; i < index; i++) printf("%c", s[i]);
    printf("\n");

    return 0;
}