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

目前的方案是使用哈希函数，使用hash值区分不同对象（通常不论是什么类型，对应的哈希函数是一种整型对象）。所以就可以用hash转换出序号。比如，常用hash对length取余，得到一个0~(length-1)的序号，然后就可以插入了。

那你也许会意识到，一个hash函数处理后可能两个不同的元素被映射到同一个序号上？这种问题被称为“哈希冲突”。

最常用的方案是间接寻址法（比如把key-value存到往后一格、两格……总之是到后面正好空着的位置。总之先来后到，直到n个元素正好装进大小为n的数组）和链表法（数组的每个index里存一个新的链表的头节点，每次出现新元素就往这个链表追加一个节点）。例如，Python的dict用间接寻址法，Java的hashmap用链表法。

不过需要注意一点，使用链表法的时候，也许`index=1`的头节点后面追加了二十个节点，结果`index=2`的头节点后面什么都没有，数组里压根就是个NULL，没有头指针。

这里很有意思，把数组和链表结合在一起了。试试吧。

## 7 树

- 树是n个节点的有限集
  - 当n=0时称为空树
  - 在任意一个非空树中
    - 有且仅有一个特定的没有上级节点的节点称为根节点root
    - 当n>1时，其余节点可分为若干的互不相交的有限集。每一个这样分出来的集合本身也是一个树，也就是root的子树

我们称节点的子节点为孩子节点，最末端的节点没有孩子节点，就被叫做叶子结点leaf。

父节点和孩子节点不用说。另外，拥有同一个父节点的n个节点称为兄弟节点sibling（需要注意哦！这里没有说n<=2。如果真的完全不超过2，那就是二叉树了。换言之，这种树可以有很多兄弟节点）

### 二叉树

二叉树`binary tree`是树的一种特殊形式，每个节点最多有2个孩子节点。也就是说，一个节点最多有1个兄弟节点。这样我们就可以给一个节点分出左孩子left child和右孩子right child。`这两个孩子节点顺序是固定的。`

一个二叉树的所有非叶子结点都有左孩子右孩子`（也就是说每个节点都充满了）`，同时，所有`叶子节点在同一层级上`，就称为`满二叉树`。

满二叉树的条件似乎有一点苛刻，有没有相对松一点的二叉树？有的兄弟，有的。

完全二叉树：对于一个有n个节点的二叉树，按层级序号编号，所有节点的编号从1~n。如果这个数所有节点和同样深度的满二叉树的节点位置相同，就称为完全二叉树。

（这个概念像是从结果反推出来的），所以我们试着从思路上理解：按层级排，第一层——第二层——……这样排下去，每次路过的时候都排满。

怎么存储二叉树？很显然，顺序存储结构和链式存储结构仍然都可以。

链式存储结构的很容易理解，直接让parent node指向两个child node就好了。C语言接着指针，Python接着直接调用对象就行。数组呢？为了让下标存在某种统一的规律，显然，我们最好按满二叉树去设计。可以试着证明一下（比如利用$1+2+4+……+2^n = {2^n-1}$）。总之，最后会发现，对于一个下标为`n`的`parent node`，他的`left child`下标是$2^n+1$，`right child`下标是$2^n+2$。

又很显然，如果是很稀疏的二叉树，按照满二叉树去用数组存储，就会有很多空间存一堆NULL，None之类的东西（因为要占位，但毕竟没东西嘛）。显然，这样的读写效率非常之快，但是占用很多空间。这就是典型的用空间换时间。而约满的二叉树，这种implementation效果就越好。比如我们后面会学的二叉堆。

```python
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# 这里我们用递归的方式实现创建

def create_binary_tree(input_list: list = []):
    if input_list is None or len(input_list) == 0:
        return None
    data = input_list.pop(0)
    if data is None:
        return None 
    node = TreeNode(data=data)
    node.left = create_binary_tree(input_list=input_list)
    node.right = create_binary_tree(input_list=input_list)
    return node
```

这里其实就是一直填下去。那你可能会问，那不就全插到左节点了吗？

这个`if input_list is none`就是神来之笔，会在到leaf的时候自动停下，返回Node。其实这就是从前序遍历创建二叉树。

### 二叉查找树

二叉树最常用的场景是在搜索查找过程中。有一种特殊的二叉树叫二叉查找树，binary search tree。二叉查找树又加上了左子树不为空，则左子树一定要小于当前根节点；右子树不为空，则右子树一定要大于当前根节点。这样一来就可以每次都实现一次二分查找，可以很简单的进行查找。

对于一个节点均衡的二叉查找树来说（先不用管这是什么意思，总之是很理想的情况），容易发现，最理想的情况下，每次都会排除一般的元素。找到想要的元素只需要花$O(logn)$的时间。

也能发现，二叉查找树其实在一定程度上反映出了当前所有元素的排序，所以也叫二叉排序树。想要解决这个问题，就需要保证二叉树能维持自身平衡。这个特性成为二叉树的自平衡。二叉树自平衡方式有很多种，比如红黑树、AVL树、树堆等。

### 二叉树的遍历

- 深度优先遍历
  - 前序遍历
  - 中序遍历
  - 后序遍历
- 广度优先遍历
  - 层序遍历

深度优先遍历就是从一点开始，彻底搜索完再遍历下一点。

以

- 1
  - 2
    - 4
    - 5
  - 3
    - 6

这个树为例

x序遍历的x可以理解为root在前/中/后

- 前序遍历
  - 顺序为：root-左子树-右子树
  - 得到1、2、4、5、3、6；
- 中序遍历
  - 顺序为：左子树-root-右子树
  - 得到4、2、5、1、3、6
- 后序遍历
  - 顺序为左子树、右子树、root
  - 4、5、2、6、3、1

我们尝试实现各种遍历。


```python
def iter_tree_implementation_one(tree: TreeNode):
    if tree is None:
        return None
    print(tree.data)
    iter_tree_implementation_one(tree=tree.left)
    iter_tree_implementation_one(tree=tree.right)
    return TreeNode


def iter_tree_implementation_two(tree: TreeNode):
    if tree is None:
        return None
    iter_tree_implementation_two(tree=tree.left)
    print(tree.data)
    iter_tree_implementation_two(tree=tree.right)
    return TreeNode


def iter_tree_implementation_three(tree: TreeNode):
    if tree is None:
        return None
    iter_tree_implementation_three(tree=tree.left)
    iter_tree_implementation_three(tree=tree.right)
    print(tree.data)
    return TreeNode
```

由此就可以得出三种遍历方式。

这里我们都用了递归。很显然，递归有回溯的特性，而栈恰好也有这种特性。

### 利用栈实现前序遍历

这里是怎么做的？实际上就是，在遇到该回头的时候（左孩子没有孩子节点的时候回溯对应的父节点，然后输出他的右孩子）。

绝大多数递归可以实现的东西都可以用栈实现，因为栈也拥有回溯的特性。我们试试看：

### 用队列实现广度优先遍历

广度优先搜索比起深度优先搜索，有个很坏的问题，在于广度搜索的每个节点本身没啥关系，不像深度搜索直接利用引用或者指针left、right。

那咋办？

可以用队列。队列这种“谁先进来就先处理谁，剩下的缓存先放着，等下再办”正好适合广度优先的缓存策略。对比栈那样子“一条路走到黑，然后一次返回一点，利用回溯功能一点点试”，很能体现二者的特性。

能感觉到，dfs就像不撞南墙不回头，撞了慢慢回。无他，`舔狗`；bfs就像每个都试探一点，不行了再一点点每个慢慢投入精力。无他，`纯钓`。dfs每次回头一点，借助栈stack的FILO回溯性、bfs则借队列queue的FIFO实现。（当然，其实bfs也有用递归或者FILO实现的方式，只是这里不再赘述）

试试实现：

```python
def iter_tree_implementation_four(node: TreeNode):
    stack = []
    result = []
    while (not (node is None)) or stack:
        while not (node is None):
            print(node.data)
            result.append(node)
            stack.append(node)
            node = node.left
        # 先把所有左边的处理到底，并且所有出现过的节点都被存储
        node = stack.pop().right
```

### 二叉堆

二叉堆本质上是一种完全二叉树，就是之前说的每个出现的节点都和满二叉树位置、序号相同的二叉树。

它分为最大堆和最小堆。最X堆表示任何一个父节点的值都大于或小于（总之是X于）他的两个孩子节点的值。也就是实现了自己维持某种平衡的完全二叉树。根节点叫做堆顶。二叉堆的性质已经决定了堆顶就是最大/最小，总之是最X项。

显然，对于二叉堆，有插入节点、删除节点和构建操作。都建立在堆的自我调整之上。

插入节点可以先插入到最后一个位置，然后和上级比较，决定和上级是否互换位置。最终上浮到合理的位置。

同理，删除节点可以先把最后一个节点拿到对应的位置上来，然后再用下沉的方式把这个节点排序到合适的位置。

构建二叉堆，也就是把一个无序的完全二叉树调整为二叉堆，本质上是让所有非叶子结点下沉到合适的位置。从最后一个非叶子节点开始（也就是倒数第二级节点）依次向上比较即可。

考虑到二叉堆是完全二叉树，所以其实已经排列很满了。加上读取次数通常大、写时往往不会大量移动，所以惯例上仍然采用数组进行存储。

在这里我们引入一个新的模块，叫binarytree。

```python
from binarytree import Node

def create_tree_from_list(input_list: list):
    if (not input_list) or (input_list is None):
        return None
    data = input_list.pop(0)
    if data is None:
        return None
    node = Node(data)
    node.left = create_tree_from_list(input_list=input_list)
    node.right = create_tree_from_list(input_list=input_list)
    return node

tree = create_tree_from_list([1, 2, 3, None, None, 4, None, None, 5, 6, None, None, 7, None , None])
print(tree)
```

可以看到，为啥用这玩意儿呢？因为输出结果可视化以后很方便看（）。

接下来想想怎么排序？
