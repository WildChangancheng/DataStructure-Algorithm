#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node{
    int data;
    struct Node *next;
} Node;

typedef struct linked_list
{
    int size;
    struct Node *head;
    struct Node *tail;
} linked_list;

// 函数声明（解决顺序问题）
void show(linked_list* list);
void free_linked_list(linked_list* list);

Node* create_node(int data) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->data = data;
    new_node->next = NULL;
    return new_node;
}

void init_linked_list(linked_list* list) {
    list->size = 0;
    list->head = NULL;
    list->tail = NULL;
}

bool is_valid_index(linked_list* list, int index) {
    return ((index >= 0) && (index < list->size));
}

Node* get_node_with_index(linked_list* list, int index) {
    if (!is_valid_index(list, index)) exit(-1);
    Node* current_node = list->head;
    for (int i = 0; i < index; i++) current_node = current_node->next;
    return current_node;
}

void insert(linked_list* list, int data, int index) {
    if (index < 0 || index > list->size) {
        printf("错误: 索引 %d 超出范围 (大小: %d)\n", index, list->size);
        return;
    }
    
    Node* new_node = create_node(data);
    
    if (list->size == 0) {
        list->head = new_node;
        list->tail = new_node;
        list->size = 1;
    } else if (index == list->size) {
        list->tail->next = new_node;
        list->tail = new_node;
        list->size++;
    } else if (index == 0) {
        new_node->next = list->head;
        list->head = new_node;
        list->size++;
    } else {
        Node* prev_node = get_node_with_index(list, index - 1);
        new_node->next = prev_node->next;
        prev_node->next = new_node;
        list->size++;
    }
}

void delete(linked_list* list, int index) {
    if (!is_valid_index(list, index)) {
        printf("错误: 索引 %d 超出范围 (大小: %d)\n", index, list->size);
        return;
    }
    
    if (index == 0) {
        Node* node_to_delete = list->head;
        list->head = node_to_delete->next;
        
        if (list->size == 1) {
            list->tail = NULL;
        }
        
        free(node_to_delete);
        list->size--;
    } else if (index == list->size - 1) {
        Node* prev_node = get_node_with_index(list, index - 1);
        Node* node_to_delete = list->tail;
        
        prev_node->next = NULL;
        list->tail = prev_node;
        
        free(node_to_delete);
        list->size--;
    } else {
        Node* prev_node = get_node_with_index(list, index - 1);
        Node* node_to_delete = prev_node->next;
        Node* next_node = node_to_delete->next;
        
        prev_node->next = next_node;
        free(node_to_delete);
        list->size--;
    }
}

// 显示链表内容
void show(linked_list* list) {
    Node* current_node = list->head;
    
    while (current_node != NULL) {
        printf("%d", current_node->data);
        if (current_node->next != NULL) {
            printf(" -> ");
        }
        current_node = current_node->next;
    }
    printf("\n");
}

// 释放链表内存
void free_linked_list(linked_list* list) {
    Node* current_node = list->head;
    
    while (current_node != NULL) {
        Node* next_node = current_node->next;
        free(current_node);
        current_node = next_node;
    }
    
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
}

void test_linked_list() {
    printf("==================================================\n");
    printf("Starting Linked List Implementation Test\n");
    printf("==================================================\n");
    
    linked_list ll;
    init_linked_list(&ll);
    
    // Test 1: Create empty linked list
    printf("\n1. Testing empty linked list:\n");
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 2: Insert first element
    printf("\n2. Testing first element insertion:\n");
    insert(&ll, 10, 0);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 3: Insert elements at the end
    printf("\n3. Testing insertion at the end:\n");
    insert(&ll, 20, 1);
    insert(&ll, 30, 2);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 4: Insert element at the head
    printf("\n4. Testing insertion at the head:\n");
    insert(&ll, 5, 0);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 5: Insert elements in the middle
    printf("\n5. Testing insertion in the middle:\n");
    insert(&ll, 15, 2);
    insert(&ll, 25, 4);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 6: Delete head element
    printf("\n6. Testing head deletion:\n");
    delete(&ll, 0);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 7: Delete tail element
    printf("\n7. Testing tail deletion:\n");
    delete(&ll, 4);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 8: Delete middle element
    printf("\n8. Testing middle element deletion:\n");
    delete(&ll, 1);
    printf("List size: %d\n", ll.size);
    show(&ll);
    
    // Test 9: Boundary case testing
    printf("\n9. Testing last element deletion:\n");
    linked_list ll2;
    init_linked_list(&ll2);
    insert(&ll2, 100, 0);
    delete(&ll2, 0);
    printf("List size: %d\n", ll2.size);
    show(&ll2);
    printf("head: %p, tail: %p\n", (void*)ll2.head, (void*)ll2.tail);
    
    free_linked_list(&ll2);
    
    // Test 10: Exception case testing
    printf("\n10. Testing exception cases:\n");
    insert(&ll, 999, 10);
    delete(&ll, 10);
    delete(&ll, -1);
    
    // Test 11: Complex operation sequence
    printf("\n11. Testing complex operation sequence:\n");
    linked_list ll3;
    init_linked_list(&ll3);
    
    for (int i = 0; i < 5; i++) {
        insert(&ll3, i * 10, i);
    }
    printf("Initial linked list:\n");
    show(&ll3);
    
    delete(&ll3, 2);
    insert(&ll3, 25, 2);
    insert(&ll3, 5, 0);
    delete(&ll3, 4);
    insert(&ll3, 35, 4);
    
    printf("Linked list after operations:\n");
    show(&ll3);
    
    // Test 12: Verify linked list connection correctness
    printf("\n12. Verifying linked list connection correctness:\n");
    Node* current = ll3.head;
    printf("Traversing linked list:\n");
    while (current) {
        printf("Node data: %d, Next node: ", current->data);
        if (current->next) {
            printf("%d\n", current->next->data);
        } else {
            printf("NULL\n");
        }
        current = current->next;
    }
    
    free_linked_list(&ll3);
    free_linked_list(&ll);
    
    printf("==================================================\n");
    printf("Testing completed!\n");
    printf("==================================================\n");
}

int main(void) {
    // 基本测试
    linked_list link;
    init_linked_list(&link);
    
    insert(&link, 1, 0);
    insert(&link, 2, 1);
    insert(&link, 4, 2);
    insert(&link, 3, 2);
    
    printf("Test begins:\n");
    show(&link);
    
    free_linked_list(&link);
    
    // 运行完整测试
    test_linked_list();
    
    return 0;
}