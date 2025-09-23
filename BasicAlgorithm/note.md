# note

## 0 前言

考虑到课程乱七八糟，难度不平滑等问题，特此增设基础算法分支。该分支难度低，内容浅显易懂，作为课程正篇的前置内容，辅助学习。

这里用Python和C语言双实现。

后续应该会加入CPP，但Rust暂无规划。

如果你刷到这个repository，可以视情况跟练对应的语言。总之，练习的时候可以不必很严谨深究这些概念。

### 0.1 过程中的编程tip

#### C 语言部分

> 1 stdlib的内存分配

>

#### Python部分

> 1 range尽量用0作为start

如果当前已经在第0项时，遍历一个序列怎么做？不要写`range(1, index)`，而是写`range(0, index)`。否则当index为1的时候，本来需要遍历一次，却得到`(1, 1)`这个空结果，仍然少遍历一次。`(0, 0)`自己就会浪费一次。

## 1 算法概述

算法有简单和低效之分，简单和复杂之分。我们从时间复杂度和空间复杂度两个角度进行量化。

从时间的角度，我们定义了渐进时间复杂度，也就是asymptopic time complexity。常常使用大O符号。根据无穷极限抓大头，实际上就是保留最高阶项并删去常数。

## 2 还tm是数组

数组是有限个相同类型的变量所组成的有序集合，每一个变量成为元素，英语是array。数组是顺序存储的。先用Python写一个：

```python
# arrary/array.py
class Array:
    def __init__(self, max_length: int =20):
        self.__length = 0
        self.__max_length = max_length
        self.__content = []
    def __is_valid_index(self, index:int) -> bool:
        return ((index<self.__max_length) and (index >= 0))
    def show(self) -> None:
        pprint(self.__content)
    def read(self, index:int):
        if not self.__is_valid_index(index=index):
            raise IndexError("Invalid index of this array.")
        if index > self.__length:
            raise IndexError("Invalid index of this array.")
        return self.__content[index]
    def insert(self, index:int, value:Any) -> None:
        if not self.__is_valid_index(index=index):
            raise IndexError("Invalid index of this array.")
        if index > self.__length:
            raise IndexError("Invalid index of this array.")
        if index == self.__length:
            self.__content.append(value)
            self.__length += 1
            return 
        self.__content.append(0)
        for i in range(index, self.__length+1)[::-1]:
            self.__content[i] = self.__content[i-1]
        self.__content[index] = value
        self.__length += 1
        return 
    def delete(self, index:int)->None:
        if not self.__is_valid_index(index=index):
            raise IndexError("Invalid index of this array.")
        if index >= self.__length:
            raise IndexError("Invalid index of this array.")
        if (index == (self.__length-1)):
            self.__content.pop()
            self.__length -= 1
            return 
        for i in range(index, self.__length-1):
            self.__content[i] = self.__content[i+1]
        self.__content.pop()
        self.__length -= 1
        return 
    def update(self, index:int, new_value:Any) -> None:
        self.delete(index=index)
        self.insert(index=index, value=new_value)
        return 
```

基本上实现了一个弱化版的数组。接下来，emm用C语言吧。

## 3 又是链表

回忆一下，链表是什么样的：

首先，链表有头指针和尾指针。尝试用Python实现一个单向链表：

```python
class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None
    def __is_valid_index(self, index: int) -> bool:
        return ((index >= 0) and (index < self.size))
    def __node_from_data(self, data: Any) -> Node:
        return Node(data=data)
    def get_node_with_index(self, index: int) -> Node:
        current_node: Node = self.head
        for _ in range(index):
            current_node = current_node.next
        return current_node
    def insert(self, data: Any, index: int) -> None:
        node = self.__node_from_data(data=data)
        if self.size == 0:
            self.head = node
            self.tail = node
            self.size = 1
        elif index == self.size:
            self.tail.next = node
            self.tail = node
            self.size += 1
        elif not self.__is_valid_index(index):
            raise IndexError("Index out of range")
        elif index == 0:
            node.next = self.head
            self.head = node
            self.size += 1
        else:
            pre_node = self.get_node_with_index(index-1)
            node.next = pre_node.next
            pre_node.next = node
            self.size += 1
    def delete(self, index: int)->None:
        if not self.__is_valid_index(index=index):
            raise IndexError("Index out of range")
        elif index == 0:
            node = self.head
            self.head = node.next
            self.size -= 1
            del node
        elif index == self.size - 1:
            node = self.tail
            self.tail = self.get_node_with_index(index=index-1)
            self.tail.next = None
            self.size -= 1
            del node
        else:
            pre:    Node = self.get_node_with_index(index=index)
            node:   Node = pre.next
            sub:    Node = node.next
            pre.next = sub
            self.size -= 1
            del node
    def show(self) -> None:
        current_node = self.head
        while current_node is not None:
            print(f"{current_node.data}", end='')
            if current_node.next is not None:
                print(" -> ", end='')
            current_node = current_node.next
        print("") 
```

然后试试用C语言实现一下。

```c
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
```

## 4 堆栈

气笑了是吗。我也气笑了。

其实也不见得多难，只是这和学的还有实验有个蛋的关系，纯靠过往的功力和自学。

加油吧，等学校实在是不现实。

记一句刚听到蛮好的歌词

> “祝你走过风雨之后留下的不是伤心模样”
> 
> 别用健康兑换虚拟浮囊
> 
> 要放下执念看星光
> 
> 星空不会嘲笑失败者的洒脱与坦荡
> 
> 放下过往，世界很大，不止眼前的悲伤
>
> 终有一天你我都能点亮自己那束光
>
> ——馄饨皮茄总《\<Lemon\>劝你别读博》

stack栈是一种线性数据结构，他就像一个储物罐，先放进去的东西够不到，只能先取出那些后放进去的东西，才能取出。这种特性允许元素先入后出(FirstInLastOut，也就是FILO)。最早进入的元素存放的位置叫栈底（就像罐子的底部），最后放入的位置就是栈顶，对应bottom和top。

思考：实际上栈这种ADT，用数组和链表似乎都能实现。所以你看，事实上，`ADT`实际上更强调`逻辑结构`，而不是很在乎`存储结构`（也就是有些教材里的`物理结构`）

栈强调入栈push操作和出栈pop操作。容易想到，最早进去的元素位置就是栈底，新放入的元素就成为新的栈顶。

在Python中实在有点简单，包装一下list就行，~~而且感觉还更难用了（）~~，不过还是意思意思好了。

```python

class Stack:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity: int = capacity
        self.bottom_index: int = 0
        self.top_index: int = -1
        self.content: list = [None for i in range(capacity)]
    
    def __is_not_full(self) -> bool:
        return (self.top_index + 1) < self.capacity  # 修正：应该是 self.capacity
    
    def show(self) -> None:
        tmp = [str(i) if i is not None else "None" for i in self.content]  # 修正：self.content
        tmp[self.bottom_index] += " (bottom)"  # 修正：self.bottom_index
        if self.top_index >= 0:  # 添加边界检查
            tmp[self.top_index] += " (top)"
        pprint(tmp)
    
    def pop(self):
        if self.top_index < 0:  # 添加空栈检查
            raise IndexError("Pop from empty stack")
        data = self.content[self.top_index]
        self.content[self.top_index] = None  # 清空位置
        self.top_index -= 1
        return data
    
    def push(self, data) -> None:
        if not self.__is_not_full():
            raise IndexError("Stack is full")
        self.top_index += 1
        self.content[self.top_index] = data
```

## 5 队列

好了，爽完了就该看队列了。队列就像是隧道，一头进一头出，里面只能单向通过——所以是先入先出(FirstInFirstOut, FIFO)。队列的出口端叫队头front，入口端叫队尾rear。

当然，肯定两种数据结构都可以实现。

入队操作中，新元素放在rear的位置，然后rear往后一个位置（所以rear一直是不放queue中的元素的）；出队操作是把front位置的元素去掉后front标记挪到新位置（所以说，front是队伍中存在的元素。）

在用数组实现的队列中，考虑到数组的空间是固定的，但是标记一直在挪动，所以我们会让标记挪动，也就是所谓的`循环队列`。

！！！这时`(rear+1)%capacity == front`可以用来判断是否成立。

事实上，Python已经给出了很多队列工具，比如`collections.deque`和`queue.Queue`。

我们试着写一个。当然，以后用到的话基本就用Python官方的了。

```python
class Queue:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.front = 0
        self.rear = 0
        self.capacity = capacity
        self.size = 0
        self.content = [None for i in range(capacity)]
    
    def show(self):
        tmp = []
        for i in range(self.capacity):
            element = self.content[i]
            tags = []
            if i == self.front and self.size > 0:
                tags.append("(front)")
            if i == self.rear:
                tags.append("(rear)")
            if element is not None:
                tmp.append(f"{element}{''.join(tags)}")
            else:
                tmp.append(f"None{''.join(tags)}")
        print("Queue: [" + " | ".join(tmp) + "]")
        print(f"Size: {self.size}, Front: {self.front}, Rear: {self.rear}")
    
    def __is_not_full(self) -> bool:
        return self.size < self.capacity
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def enqueue(self, element):
        if not self.__is_not_full():
            raise ValueError("Queue is full")
        self.content[self.rear] = element
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise ValueError("Queue is empty")
        element = self.content[self.front]
        self.content[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return element
```

这里需要注意一件事，写dequeue的时候，之前删除元素都是从后面删掉，所以下标往前；这里是从前除名元素，所以应该让下标+=1.

## 6 哈希表

哈希表hashmap也叫散列表，提供了键key和值value的映射关系，只要给出key，就可以给出对应的value。（用Python的dict去想）

哈希表的核心目的在于查询，换言之，需要查询效率尽可能高。在之前学过的基础数据类型中，我们能明显发现，用数组的效率是最高的。所以我们不妨就使用数组：于是问题在于，怎么给元素找对应的数组下标？

目前的方案是使用哈希函数，使用hash值区分不同对象（通常不论是什么类型，对应的哈希函数是一种整型对象）。

最常用的方案是