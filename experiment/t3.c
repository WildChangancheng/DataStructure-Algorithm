#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef struct node
{
    struct node* left, *right;
    int value;
} node;


node* new_node(int value) {
    node* n = (node*)malloc(sizeof(node));
    n->value = value;
    n->left = n->right = NULL;
    return n;
}


node* create_tree_from_tokens(char* tokens[], int* index, int n) {
    if (*index >= n) return NULL;

    char* token = tokens[*index];
    (*index)++;

    if (strcmp(token, "#") == 0) {
        return NULL;
    }

    int val = atoi(token);
    node* root = new_node(val);

    root->left  = create_tree_from_tokens(tokens, index, n);
    root->right = create_tree_from_tokens(tokens, index, n);

    return root;
}


node* jiaoji_trees(node* t1, node* t2) {
    if (t1 == NULL || t2 == NULL) return NULL;

    node* root = new_node(t1->value + t2->value);
    root->left  = jiaoji_trees(t1->left, t2->left);
    root->right = jiaoji_trees(t1->right, t2->right);

    return root;
}


void inorder(node* root, bool *first) {
    if (root == NULL) return;
    inorder(root->left, first);
    if (*first) {
        printf("%d", root->value);   // 第一个数不输出空格
        *first = false;
    } else {
        printf(" %d", root->value);  // 后面的数前面加空格
    }
    inorder(root->right, first);
}


int main()
{
    // char s[100];
    // char result[100];
    // char ch;

    // int index = 0;
    // bool flag = true;

    // if (fgets(s, sizeof(s), stdin) != NULL) {
    //     for (int i = 0; s[i] != '\0'; i++) {
    //         if (s[i] != ' ' && s[i] != '\t' && s[i]!='\n')   result[index++] = s[i];
    //     }
    // }
    // 输入10 5 2 # # 8 # # 20 # 30 # #
    // 得到1052##8##20#30##（删掉空格打印，总之输入没问题）
    // 现在的index就是元素个数

    char input1[200], input2[200];
    fgets(input1, sizeof(input1), stdin);
    fgets(input2, sizeof(input2), stdin);

    // -------- 处理第一棵树 --------
    char* tokens1[100];
    int n1 = 0;
    char* tok = strtok(input1, " \t\n");
    while (tok != NULL) {
        tokens1[n1++] = tok;
        tok = strtok(NULL, " \t\n");
    }
    int idx1 = 0;
    node* t1 = create_tree_from_tokens(tokens1, &idx1, n1);

    char* tokens2[100];
    int n2 = 0;
    tok = strtok(input2, " \t\n");
    while (tok != NULL) {
        tokens2[n2++] = tok;
        tok = strtok(NULL, " \t\n");
    }
    int idx2 = 0;
    node* t2 = create_tree_from_tokens(tokens2, &idx2, n2);
    node* t_jiaoji = jiaoji_trees(t1, t2);

    bool first = true;
    inorder(t_jiaoji, &first);
    printf("\n");
    printf("\n");

    return 0;
}