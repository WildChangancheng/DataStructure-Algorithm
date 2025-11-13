# note

## Day01 关于算法与本章节

是学习Labuladong的算法笔记 过程中产出的摘要与思考。以速成为主。Day01量力而行，不求一步到位——每次能看懂多少看多少，多看几次。

在DSA课程中，遇到的所有数据结构基本都可以看成`顺序存储结构` 和 `链式存储结构`的延伸与扩展。这里我们需要理解一件事，平时我们说的`人工智能的xx算法`之类更多侧重数学上构建合适的模型之类，是综合运用各方面能力产出的结果；DSA课程中的算法更侧重于计算机基本功，能让你写出更优美、高效的程序，是基础性的。

在DSA课程的层面上，我们往往可以站在”穷举“的角度考虑问题。分析怎么能更好地`穷举`。最基本的要求是访问解空间中的所有情况——`无遗漏`，在此之上，我们可以要求`少重复`——比如剪枝之类。例如：”树上有多少叶子？“——摘下来的一片 和 剩下的还在树上的一片。树上剩下多少？再重复这个过程——用迭归的方式实现遍历。

补：要有框架思维，学会提炼重点，寻找不变量，把凝结成的思维精华变成可复用的方法论。哪怕快睡着的时候，写出来的代码也不会太过于离谱。

### 1.1 顺序存储结构与链式存储结构基础

很多地方，我们会看到`数组`这种表述。我们这里的`顺序存储结构`这个数组指的是一块连续的内存空间，我们可以通过索引来访问这块内存空间中的元素，这才是数组的原始形态。而编程语言封装好的，添加了诸如push、insert之类API的数组就更高级一些。

静态数组在创建的时候就要确定数组的元素类型和元素数量。只有在 C++、Java、Golang 这类语言中才提供了创建静态数组的方式。类似 Python、JavaScript 这类语言并没有提供静态数组的定义方式。静态数组的用法比较原始，实际软件开发中很少用到，写算法题也没必要用，我们一般直接用动态数组。不过我们从静态数组开始。

用C语言说:

```c
int arr[10];
memset(arr, 0, sizeof(arr));
```

这里的memset接受一个地址，一个值和一个长度。他会把这个地址之后相应的长度全都换成对应的值，也就是把一段memory set为合适的value，所以叫memset。包含于string.h。

在早期的C语言标准中，arr[10]必须在最开始就定下来是10。直到C99，引入了变长数组VLA，允许数组的长度在运行时动态确定，而不是在编译时固定。它的主要特点包括动态长度、栈内存分配。通常来说，我们认为C++到处都是C语言的超集。但是，C语言不支持变长数组。也就是说，这是极其罕见的例外，C语言支持但是CPP不支持。CPP使用Vector替代实现相应功能。

用Python的话：Python其实不支持变长数组，但我们可以手动伪造一个：

```python
lst = [0 for i in range(10)]
```

### 1.2 顺序存储结构的增删改查

#### 查（访问）

如果我们写：

```c
arr[1] = 1;
```

这里出现退化现象，`arr[1]`是语法糖，相当于`*(arr+1)`。其中的`arr`退化为`&arr[0]`。我们用eg1.c做一个实验:

```c
// eg1.c
#include <stdio.h>
#include <string.h>

int main() {
    int arr[10];
    memset(arr, 0, sizeof(int) * 4);

    arr[1] = 1;
    *(&arr[0] + 2) = 2;
    printf("%d\n%d\n", arr[1], arr[2]);
    return 0;
}
```

输出结果是1和2，符合预期。如果不用memset初始化的话，在C、CPP中如果访问了3~9的这些没有指定值的位置，就不一定会得到什么了。

在这个过程中，我们知道一个作为基准的地址，比如`arr`在大多时候退化为`&arr[0]`。我们知道每个元素的类型后相当于知道了这种元素占用的内存空间大小，也就可以推算出所有位置，也就是`base_memory + indice * sizeof(elmenet)`，这个时间复杂度是`O(1)`，访问一个确定内存的时间复杂度也是`O(1)`，所以数组的时间复杂度是`O(1)+O(1) = O(1)`

#### 增

数组的增需要分情况讨论。如果是说append（在最后追加），显然只要知道当前存储的元素总数，也就是length，然后直接访问`arr[length]`改数值就可以了，时间复杂度是`O(1)`

如果是insert，也就是在数组中间的位置插入元素，那就需要把索引indice后面的元素都往后挪1个位置，然后把数据插在这个空位。综上，在数组中插入元素的时间复杂度是`O(N)`

如果数组已经满了，那么报错的话就是`O(1)`，想要把所有数据都挪到更大的地方，就需要`O(N)`

#### 删

删除元素的操作和增加元素的操作类似，在最后删除是`O(1)`，删除中间元素是`O(N)`。

Python的list本身就比较高级，不需要做什么升级。这里补充一下CPP的vector。

```cpp
vector[int] arr;
// declaration of a vector

arr.push_back(1);
arr.push_back(3);
// append a new element

arr.insert(arr.begin()+2, 2);
// insert 2 at the second posistion of arr

arr.pop_back();
// delete the last element

arr.erase(arr.begin());
// delete the first element
```

### 1.3 链式存储结构的增删改查

一条链表并不需要一整块连续的内存空间存储元素。链表的元素可以分散在内存空间的天涯海角，通过每个节点上的 next, prev 指针，将零散的内存块串联起来形成一个链式结构。它的节点要用的时候就能接上，不用的时候拆掉就行了，从来不需要考虑扩缩容和数据搬移的问题，理论上讲，链表是没有容量限制的。

显然，链表适合大量编辑的情况。在高频访问的情形下，链表就远不如顺序存储结构了，因为只能顺着指针一个个读，直到真的到达第n个。

我们管具有自身的`val`和指向下一个节点的指针的`next`的链表成为`单链表`；在单链表基础上，还能往回指，具有`prev`这个指向前一个节点的字段的链表称为双链表。

我们可以把链表看成孤立的节点，通过“连线”将他们连起来。对于Python或者Java之类的语言，这条线就是引用；对于C或者C++这样的语言，这条线就是指针。

### 1.4 时空复杂度分析基础

先说分析复杂度的数学模型

- P问题与NP问题
  - P问题是多项式时间可解的问题
  - NP问题是多项式时间不可解的问题
  - 很显然是NP问题多，不过这不在当前范围内
- 渐进效率
  - 输入规模非常大的时候（毕竟要是数据量小，随便用什么算法差距也拉不开多大）
  - 根据高数的知识，很容易知道，对于一元函数来说，自变量很大时，函数大小更多在于`最高阶项`：重要的是`阶`
  - 用Theta表示同阶函数集合
  - 用big-O表示低阶函数集合（让`表示复杂度的函数`变成F(n)的低阶项，其实是说`F(n)是复杂度函数的高阶`，也就是`O(F(n))`其实是在给复杂度函数找上界）
  - 用big-Omega表示高阶函数集合（也就是找下界）
- 一些小tip
  - 我们发现，实际上那些标记都是一些集合。但是为了写起来方便，我们用`=`替代`属于符号`。所以用`f(n) = O(g(n))`表示f(n)是g(n)的低阶函数集合中的元素，也就是f(n)是g(n)的低阶函数。
  - 我们还发现，big-O和big-Omega符号表示的函数集合其实都不严格，也就是包含了同阶的情况（Theta符号弱于这两个符号）。所以我们选用了small-O和small-Omega表示严格低阶/高阶函数集合，取消了等于号的存在。
  - 另外，其实不是所有函数都是可比的。比如`n`和`n^(1+sin n)`就没法比
  - 很显然，分析big-O符号的时候就可以按着最坏情况考虑；分析big-Sigma符号的时候就可以按最好情况考虑。

加法法则与乘法法则

设𝑻_𝟏 (𝒏)=𝑶(𝒇(𝒏)), 𝑻_𝟐 (𝒏)=𝑶(𝒈(𝒏)), 则
加法规则：𝑻_𝟏 (𝒏)+𝑻_𝟐 (𝒏)=𝑶(𝒎𝒂𝒙{𝒇(𝒏), 𝒈(𝒏)})
乘法规则：𝑻_𝟏 (𝒏)∗𝑻_𝟐 (𝒏)=𝑶(𝒇(𝒏)∗𝒈(𝒏))

再说常见情形的处理方式。

- 赋值语句 & 读写语句
  - 运行时间通常取O(1)。有函数调用的除外，此时要考虑函数的执行时间
- 语句序列
  - 使用加法规则，所以按序列中耗时最多的语句的运行时间计算
- 分支语句
  - 运行时间由条件测试 (通常为O(1)) 加上分支中运行时间最长的语句的运行时间
- 循环语句
  - 运行时间是对输入数据重复执行n次循环体所耗时间的总和；
  - 通常，将常数因子忽略不计，可以认为上述时间是循环重复次数n和m的乘积，其中m是n次执行循环体当中时间消耗多的那一次的运行时间 (乘法规则)
- 函数调用语句
  - 若程序中只有非递归调用，则从没有函数调用的被调函数开始，计算所有这种函数的运行时间；
  - 若程序中有递归调用，则令每个递归函数对应于一个未知的时间开销函数T(n)，其中n是该函数参数的大小，之后列出关于T的递归方程并求解之。

## Day02 数组与链表基础

### 2.1 手动实现封装过的数组

我们要做的主要是

- 自动扩容与缩容
  - 当数组元素个数达到底层静态数组的容量上限时，扩容为原来的 2 倍；
  - 当数组元素个数缩减到底层静态数组的容量的 1/4 时，缩容为原来的 1/2。
- 越界检查
  - 检查一个索引是不是合法值，有没有超过合理的范围
- 删除元素防止内存泄漏
  - 这个得看具体的语言，比如Java看到元素的值被设定为null才会彻底释放它，否则会认为引用一直存在，而不回收
  - 这个咱们知道就行，暂时不深究

Python：

没咋写，看网站源码就行。

C:

```c
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef struct arr
{
    int *content;
    int size;
    // 已用容量
    int capacity;
    // 理论容量
} arr;

arr* create_arr(int capacity) {
    arr *array = (arr*) malloc(sizeof(arr));  // 分配结构体本身
    array->size = 0;
    array->capacity = capacity;
    array->content = (int*) calloc(capacity, sizeof(int));  // 分配元素空间
    // 这里要注意，不可以前面都写array，结果后面返回对array取址
    // 因为那样的话array就是临时变量，等函数执行完就销毁了
    return array;
}

arr* resize(arr* array, int new_size) {
    arr* new_array = create_arr(new_size);

    for (int i = 0; i < array->size; i++) new_array->content[i] = array->content[i];
    new_array -> size = array -> size;

    free(array->content);
    free(array);

    return new_array;
}


bool is_element_index(arr* array, int index) {
    return (0 <= index)  && (index < array->size);
}

bool is_position_index(arr* array, int index) {
    return (0 <= index)  && (index <= array->size);
}

int get_size(arr* array) {
    return array->size;
}

void show_array(arr* array) {
    printf("****************************\n");
    printf("Size: %d | Capacity: %d\n", array -> size, array -> capacity);
    for (int i = 0; i < array-> size; i++) printf("number%2d -%2d ;\n", i+1, array->content[i]);
    return ;
}


arr* append(arr* array, int element) {
    if (array->size == array->capacity) array = resize(array, 2 * array->capacity);
    array -> content[array -> size] = element;
    array -> size ++;
    return array;
}

arr* add(arr* array, int index, int element){
    if (!is_position_index(array, index)) return array;

    if (array->size == array->capacity) array = resize(array, 2 * array->capacity);

    if (index < array->size) {
        for (int j = array -> size; j > index; j-- ) {
            array -> content [j] = array -> content [j-1];
        } 
        array -> content[index] = element;
        array->size++;
    } else if (index == array->size) {
        array = append(array, element);
    } else {
        return array;
    }


    return array;
}

arr* pop(arr* array) {
    array->size --;
    if (array->size<(array->capacity/4)) array = resize(array, array->capacity/2);
    array->content[array->size-1] = 0;
    return array;
}

arr* remove_index(arr* array, int index) {
    if (!is_position_index(array, index)) return array;
    if (array->size<(array->capacity/4)) array = resize(array, array->capacity/2);

    if (index < array->size) {
        for (int j = index; j < array -> size-1; j++ ) {
            array -> content [j] = array -> content [j+1];
        } 
        array -> content[array->size] = 0;
        array->size--;
    } else if (index == array->size) {
        array = pop(array);
    } else {
        return array;
    }

    return array;
}

int main() {
    arr *array = create_arr(5);

    for (int i = 0; i < 10; i++) {
        array = append(array, i);
    }

    show_array(array);
    
    array = add(array, 2, 666);
    array = add(array, 11, 666);
    show_array(array);

    array = pop(array);
    show_array(array);

    array = remove_index(array, 2);
    show_array(array);
    return 0;
}
```

### 2.2 手动实现链表

手动实现链表对应leetcode 707-Design Linked List这道题。基础内容无需多言，但是有一些小技巧。在力扣做题时，一般题目给我们传入的就是单链表的头指针。但是在实际开发中，用的都是双链表，而双链表一般会同时持有头尾节点的引用。

我们也有一些小技巧：

- 保持对头尾节点的引用
- 虚拟头尾节点
  - 这样就能保证无论如何，对所有节点的操作（包括头结点和尾节点）都一致
  - 无非就是把前面和后面连起来或者断开前面和后面然后加一个
  - 不过这里需要对外隐藏，封装的时候所有数据都不应该跟虚拟头尾节点有关

## Day03 前缀和

### 3.1 数组的前缀和

我们经常需要给一个数列求片段和。如果直接用加法，比如求前20项和，就是无脑for循环，时间复杂度是O(n)，性能有限。根据高中知识，$a_n$和$S_n$可以互转。换言之，对于片段和，咱们完全可以用前n项和作差得出。比如$a_{11}+a_{12}+…+a_{20}$可以用$S_{21}-{S_10}$一步到位。

所以我们可以构造他的前n项和数列。对于数组来说，我们可以构造前缀和数组。

```python
from typing import List

class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.sum_array = [0] + [sum(nums[0:i+1:1]) for i in range(len(nums))]
        # 这个sum说白了是偷懒的写法，其实每次还是计算了前面所有求和
        # 正确的做法是递归一下或者for一次，只需要一次计算，就可以得整个数组
        

    def sumRange(self, left: int, right: int) -> int:
        return self.sum_array[right] - self.sum_array[left]        


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)
```

这里的sum_array是讲义里是从0开始的，也就是前n项和Sn被存储在S_{n+1}里。前面有个0凑数。最坏时间复杂度一下就变成$O(1)$了。

C语言类似：

```c
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
```

上面需要专门注意一下，不要只声明一个指针而不赋值，不然得到的就是一个野指针。

再比如：

> 给你一个整数数组 nums ，请计算数组的 中心下标 。
> 数组 中心下标 是数组的一个下标，其左侧所有元素相加的和等于右侧所有元素相加的和。
> 如果中心下标位于数组最左端，那么左侧数之和视为 0 ，因为在下标的左侧不存在元素。这一点对于中心下标位于数组最右端同样适用。
> 如果数组有多个中心下标，应该返回 最靠近左边 的那一个。如果数组不存在中心下标，返回 -1 。

前缀和的精髓其实在于把孤立的个体的值换成”一段区间的和“。就像离散型随机变量的分布列与阶梯型分布函数。这道题我们完全可以用类似的思想，

如果用一般的思想：

```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        sum_array = [0] + [sum(nums[0:i+1:1]) for i in range(len(nums))]
        end = sum_array[-1]
        for i in range(len(nums)):
            if ((sum_array[i+1] - nums[i]) * 2) == (end - nums[i]):
                return i
        return -1
```

用更高级的思想：

```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left_sum = 0
        for i, num in enumerate(nums):
            if left_sum == total - left_sum - num:
                return i
            left_sum += num
        return -1
```

扣掉左边的，就是右边的。仍然是preSum的思想。

再比如给你一个整数数组 nums，返回 数组 answer ，其中 answer[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积 。不可以用除法，并请在$O(n)$时间内完成。仍然有”一段“的感觉，所以我们仍然可以用类似的思想。

总之，核心在于”利用一整段“，不要重复计算一样的过程。

### 3.2 矩阵的前缀和

同理，矩阵，或者用计算机的说法叫二维数组，也可以有前缀和。preSum的利用方法和之前说的二维随机变量分布函数相似，通过“计数贡献”，类似“德摩根定律”的方式计算。

> 304
> 给定一个二维矩阵 matrix，以下类型的多个请求：
> 计算其子矩形范围内元素的总和，该子矩阵的 左上角 为 (row1, col1) ，右下角 为 (row2, col2) 。
实现 NumMatrix 类：
> NumMatrix(int[][] matrix) 给定整数矩阵 matrix 进行初始化
> int sumRegion(int row1, int col1, int row2, int col2) 返回 左上角 (row1, col1) 、右下角 (row2, col2) 所描述的子矩阵的元素 总和 。

这道题先用Python实现一下。

```python
from typing import List 

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        column = len(matrix[0])
        row = len(matrix)
        self.f_matrix = [[0 for _ in range(column + 1)] for _ in range(row + 1)]
        
        for i in range(row):
            for j in range(column):
                self.f_matrix[i+1][j+1] = (
                    self.f_matrix[i][j+1] + 
                    self.f_matrix[i+1][j] - 
                    self.f_matrix[i][j] + 
                    matrix[i][j]
                )


    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        f = self.f_matrix
        return (
            f[row2+1][col2+1]
            - f[row1][col2+1]
            - f[row2+1][col1]
            + f[row1][col1]
        )
        


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)
```

### 3.3 前缀积

用类似的思路，我们可以很容易实现前缀积——用逆运算再拆出在某一区间上的贡献就好了。但与此同时，还有个问题：如果某一个因数是0怎么办？可以重新计数处理。

```python
class ProductOfNumbers:

    def __init__(self):
        self.prefix = [1]  # 前缀积列表

    def add(self, num: int) -> None:
        if num == 0:
            # 重置前缀积（0 之后的积重新算）
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):
            return 0  # 表示包含了某个 0
        return self.prefix[-1] // self.prefix[-1 - k]
```

## Day04 差分数组

之前我们学了前缀和数组。前缀和的精髓在于原始数组不会被修改的时候，利用一整段的操作，减少重复计算前k项和的过程。还有个类似的技巧，叫差分数组。主要适用场景是频繁对原始数组的某个区间的元素进行增减。

运用了差分数列的相关性质。对区间整体增减，不影响彼此差距，所以要修改的数据量就大大减小。回忆一下，$d_n = a_n - a_{n-1}$反推$a_n$：$d_n$的前n项和加上$a_1$就好。由于该场景下对区间整体的修改更多，所以保证修改过程快就好。还原数组的时候确实时间复杂度会稍微大一点，但是毕竟相对而言次数少，所以显得不那么重要。

## Day05 二维数组

有一点小trick。

### 5.1 原地旋转矩阵

在不开辟新空间的情况下，怎么对矩阵做原地旋转？我们需要脑洞大开一下。

从坐标来看，旋转其实就是让行变成列，所以大概率会和转置transpose有关。先做转置，然后再行反转reverse，得到的就是顺时针旋转90度的结果。同理，如果先转置transpose，然后再列反转，得到的就是逆时针旋转90度的结果。

Leetcode的T48旋转图像就是这个问题。

> 给定一个 n × n 的二维矩阵 matrix 表示一个图像。请你将图像顺时针旋转 90 度。
> 你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。
> 输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
> 输出：[[7,4,1],[8,5,2],[9,6,3]]

```python
from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                if i!=j:
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()
```

### 5.2 一点关于反转的小trick

如何原地反转一个字符串中的单词?给你一个字符串 s ，请你反转字符串中 单词 的顺序。单词 是由非空格字符组成的字符串。s 中使用至少一个空格将字符串中的 单词 分隔开。返回 单词 顺序颠倒且 单词 之间用单个空格连接的结果字符串。注意：输入字符串 s中可能会存在前导空格、尾随空格或者单词间的多个空格。返回的结果字符串中，单词间应当仅用单个空格分隔，且不包含任何额外的空格。

这种问题其实是要你站在计算机的角度思考：如何保持局部顺序不变的情况下，反正大体的顺序？

要知道，两次反转相当于无效。所以：可以先反转一次整体顺序，再把不需要反转的部分反转回去。如：

> 给你一个字符串 s ，请你反转字符串中 单词 的顺序。
> 单词 是由非空格字符组成的字符串。s 中使用至少一个空格将字符串中的 单词 分隔开。
> 返回 单词 顺序颠倒且 单词 之间用单个空格连接的结果字符串。注意：输入字符串 s中可能会存在前导空格、尾随空格或者单词间的多个空格。返回的结果字符串中，单词间应当仅用单个空格分隔，且不包含任何额外的空格。

可以一直交换倒数第一、第一个元素；倒数第二、第二个元素，最终实现倒序。

### 5.3 螺旋形遍历

其实就是右、下、左、上过程的重复，只是一直调整界限。

## Day06 环形数组 & 其他数组/链表小技巧

我们可否把数组头尾项链，形成一个圈？直观来看有点难，数组就是一块线性连续的内存空间。但是我们可以通过一定的技巧至少让他在逻辑上成环形。例如：

```python
arr = [1, 2, 3, 4, 5]
i = 0
# 模拟环形数组，这个循环永远不会结束
while i < len(arr):
    print(arr[i])
    i = (i + 1) % len(arr)
```

那具体我们怎么把环形数组构建出来呢？可以用start和end两个指针指元素，并且允许start在end之后——这种情况下，`array[start]——array[-1]`的一段应当紧接着`array[0]——array[end]`，这样就重新绕回来了。

很显然，核心代码就是最后的`i = (i + 1) % len(arr)`。这种自增方式让i永远在0~5范围内循环，而不会打破while-loop。

环形数组的一大优势在于可以很好地增删头和尾的元素（请仔细思考这是为什么，这是核心问题。相比于头尾元素，环形数组不是很擅长在一组数据的中间插入新元素），所以环形数组非常适合做双端队列。准确来说。环形数组的最大优势就是在固定空间内实现头尾两端 O(1) 的插入和删除，所以非常适合实现双端队列 (deque) 或循环缓冲区 (ring buffer)。

环形数组也可以删除指定索引的元素，也要做数据搬移，和普通数组一样，复杂度是 O(N)；环形数组也可以获取指定索引的元素（随机访问），只不过不是直接访问对应索引，而是要通过 start 计算出真实索引，但计算和访问的时间复杂度依然是O(1)；环形数组也可以在指定索引插入元素，当然也要做数据搬移，和普通数组一样，复杂度是O(N)。

### t641

这个题有点长，所以我们单独开一个趴。

> 设计实现双端队列。
> 实现 MyCircularDeque 类:
> MyCircularDeque(int k) ：构造函数,双端队列最大为 k 。
> boolean insertFront()：将一个元素添加到双端队列头部。 如果操作成功返回 true ，否则返回 false 。
> boolean insertLast() ：将一个元素添加到双端队列尾部。如果操作成功返回 true ，否则返回 false 。
> boolean deleteFront() ：从双端队列头部删除一个元素。 如果操作成功返回 true ，否则返回 false 。
> boolean deleteLast() ：从双端队列尾部删除一个元素。如果操作成功返回 true ，否则返回 false 。
> int getFront() )：从双端队列头部获得一个元素。如果双端队列为空，返回 -1 。
> int getRear() ：获得双端队列的最后一个元素。 如果双端队列为空，返回 -1 。
> boolean isEmpty() ：若双端队列为空，则返回 true ，否则返回 false  。
> boolean isFull() ：若双端队列满了，则返回 true ，否则返回 false 。

用C语言的格式：

> /**
> \* Your MyCircularDeque struct will be instantiated and called as such:
> \* MyCircularDeque\* obj = myCircularDequeCreate(k);
> \* bool param_1 = myCircularDequeInsertFront(obj, value);
> \* bool param_2 = myCircularDequeInsertLast(obj, value);
> \* bool param_3 = myCircularDequeDeleteFront(obj);
> \* bool param_4 = myCircularDequeDeleteLast(obj);
> \* int param_5 = myCircularDequeGetFront(obj);
> \* int param_6 = myCircularDequeGetRear(obj);
> \* bool param_7 = myCircularDequeIsEmpty(obj);
> \* bool param_8 = myCircularDequeIsFull(obj);
> \* myCircularDequeFree(obj);
>*/

### 双指针法

很多时候我们操作时需要在两个节点间切来切去（比如合并两个链表，在链表1和链表2的对应节点间来回操作）或者把一个二链表分成两部分，就可以使用双指针进行操作。

> T86分割链表
> 给你一个链表的头节点 head 和一个特定值 x ，请你对链表进行分隔，使得所有 小于 x 的节点都出现在 大于或等于 x 的节点之前。
> 你应当 保留 两个分区中每个节点的初始相对位置。
> 输入：head = [1,4,3,2,5,2], x = 3
> 输出：[1,2,2,4,3,5]

```c
#include <stdlib.h>
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode ListNode;

struct ListNode* partition(struct ListNode* head, int x) {
    ListNode* smallDummy = calloc(1, sizeof(ListNode)); // < x
    ListNode* largeDummy = calloc(1, sizeof(ListNode)); // >= x
    ListNode* small = smallDummy;
    ListNode* large = largeDummy;
    
    while (head != NULL) {
        ListNode* next = head->next; // 保存后继节点
        head->next = NULL;           // 断开原链表连接
        
        if (head->val < x) {
            small->next = head;
            small = small->next;
        } else {
            large->next = head;
            large = large->next;
        }
        head = next;
    }
    
    small->next = largeDummy->next;
    ListNode* result = smallDummy->next;
    
    free(smallDummy);
    free(largeDummy);
    return result;
}
```

其实就是通过同时操作多个指针进行多线操作。

## Dayo07 栈与队列

栈和队列的精髓在于FIFO和FILO。队列只能在一端插入元素，另一端删除元素；栈只能在某一端插入和删除元素。说白了就是把数组链表提供的 API 删掉了一部分，只保留头尾操作元素的 API 给你用。（也就是简化模型，得到一些最基本的模型）。

用链表作为底层数据结构实现队列和栈实在是太简单了，直接调用双链表的 API 就可以了。用数组实现栈和队列也不难，完全可以用环形数组，使得时间复杂度降为O(1)。如果把他们合起来，就是双端队列deque（queue和stack的remix）

### 作业

今天比较偷懒

```python
from collections import deque

class Solution:
    def simplifyPath(self, path: str) -> str:
        q = deque()
        lst = [i for i in path.split(r'/') if i]
        for i in lst:
            if i == '..':
                if not (len(q)):
                    continue
                q.pop()
            elif i == '.':
                pass
            else:
                q.append(i)
        return '/' + '/'.join(q)
```

```c
bool isValid(char* s) {
    char *stack = calloc(1000000, sizeof(char));
    int i = 0;
    int pointer = 0;
    while (s[i] != '\0') {
        switch (s[i]) {
            case '(':
                stack[pointer] = 1;
                pointer ++;
                break;
            case '{':
                stack[pointer] = 2;
                pointer ++;
                break;
            case '[':
                stack[pointer] = 3;
                pointer ++;
                break;
            case ')':
                pointer --;
                if (pointer<0) return false;
                if (stack[pointer] == 1) {
                    stack[pointer] = 0;
                    break;
                }
                else return false;
            case '}':
                pointer --;
                if (pointer<0) return false;
                if (stack[pointer] == 2) {
                    stack[pointer] = 0;
                    break;
                }
                else return false;
            case ']':
                pointer --;
                if (pointer<0) return false;
                if (stack[pointer] == 3) {
                    stack[pointer] = 0;
                    break;
                }
                else return false;
        }
        i++;
    }
    if (pointer == 0) return true;
    return false;
}
```

### 单调栈模板

现在给你出这么一道题：输入一个数组 nums，请你返回一个等长的结果数组，结果数组中对应索引存储着下一个更大元素，如果没有更大的元素，就存 -1。

比如说，输入一个数组 nums = [2,1,2,4,3]，你返回数组 [4,2,4,-1,-1]。因为第一个 2 后面比 2 大的数是 4; 1 后面比 1 大的数是 2；第二个 2 后面比 2 大的数是 4; 4 后面没有比 4 大的数，填 -1；3 后面没有比 3 大的数，填 -1。

这道题的暴力解法很好想到，就是对每个元素后面都进行扫描，找到第一个更大的元素就行了。但是暴力解法的时间复杂度是O(n 
2)。

### 栈的回溯性

我们之前的所有性质很大程度上都依赖于栈的回溯性->“上一个”、“记忆”之类的东西。比如“上一步路径”、逆波兰式“刚才的两个数”之类。

## Dayo08 哈希表

哈希表强调key-value成对。就像数组，数组里面每个索引都是唯一的，不可能说你这个数组有两个索引 0。至于数组里面存什么元素，随便你，没人 care；所以一个hashmap中要求key唯一，映射出的value是什么不重要。

考虑到对于查询来说，读取之类的东西肯定是数组的效率最高，所以我们想用数组进行实现。

### 8.1 哈希函数

哈希函数就是用来把任意的key转换成相应的index的。

这就意味着：增删查改的方法中都会用到哈希函数来计算索引，如果你设计的这个哈希函数复杂度是O(N)，那么哈希表的增删查改性能就会退化成O(N)，所以说这个函数的性能很关键。个函数还要保证的一点是，输入相同的 key，输出也必须要相同，这样才能保证哈希表的正确性。

总之，哈希函数的关键在于实现 `key: Any -> hash: int]`的映射。

### 8.2 哈希冲突

于是你就会想，如果两个不同的 key 通过哈希函数得到了相同的索引，怎么办呢？这种情况就叫做「哈希冲突」。哈希冲突是一定会出现的，因为这个 hash 函数相当于是把一个无穷大的空间映射到了一个有限的索引空间，所以必然会有不同的 key 映射到同一个索引上。常用的解决方法就是开放寻址法（线性探寻法）和拉链法。

拉链法相当于是哈希表的底层数组并不直接存储 value 类型，而是存储一个链表，当有多个不同的 key 映射到了同一个索引上，这些 key -> value 对儿就存储在这个链表中，这样就能解决哈希冲突的问题；而线性探查法的思路是，一个 key 发现算出来的 index 值已经被别的 key 占了，那么它就去 index + 1 的位置看看，如果还是被占了，就继续往后找，直到找到一个空的位置为止。

### 8.3 扩容和复杂因子

于是你就发现，哈希冲突终究会导致性能下降。比如用拉链法的话，所有元素全排在`hash_array[0]`指向的链表了，顺着这个链表查，时间复杂度变成O(k)了（k是这个链表的长度）。类似的，开放寻址法当然也有这个问题。

所以说，如果频繁出现哈希冲突，那么 K 的值就会增大，这个哈希表的性能就会显著下降。这是我们需要避免的。也就是`设计合理的哈希函数，使得哈希值分布尽量均匀`。除此以外，还有很重要的一点：如果一个哈希表存储的key-value太多了，就肯定会冲突很多。

前者太复杂，咱们暂时不研究。对于后者，用拉链法实现的哈希表，负载因子可以无限大，因为链表可以无限延伸；用线性探查法实现的哈希表，负载因子不会超过 1。像 Java 的 HashMap，允许我们创建哈希表时自定义负载因子，不设置的话默认是 0.75，这个值是经验值，一般保持默认就行了。当哈希表内元素达到负载因子时，哈希表会扩容。和之前讲解动态数组的实现 是类似的，就是把哈希表底层 table 数组的容量扩大，把数据搬移到新的大数组中。size 不变，table.length 增加，负载因子就减小了。

这也能解释为什么不要相信哈希表的顺序（比如Python的字典是无序的，除非专门导入collections里的有序字典OrderedDict。哈希表的遍历本质上就是遍历那个底层 table 数组。由于 hash 函数要把你的 key 进行映射，所以 key 在底层 table 数组中的分布是随机的，不像数组/链表结构那样有个明确的元素顺序。一旦发生扩容，要用 hash 函数重新计算 key 的哈希值，然后放到新的 table 数组中。而hash函数计算出的索引值关于table.length。也就是说，哈希表自动扩缩容后，同一个 key 存储在 table 的索引可能发生变化，所以遍历结果的顺序就和之前不一样了。

### 8.4 哈希链表

像是新的Go语言便利完全无序，3.7以后的Python的Dict竟然有序了。这是因为他们把数据结构换成了哈希链表。就是在哈希表的基础上套一层链表，为节点加上prev和next，从而保持他们的顺序。

虽然删除链表中的给定序号的节点时间复杂度是O(n)，但是这里删除给定双链表节点的操作只用O(1)。原理也很简单，因为哈希链表是哈希表和链表的结合，完全可以用key和哈希表得到下标，而不用挨个数。

### 8.5 哈希集合

哈希集合就是集合啦（划掉）

哈希集合关键的特性在于“去重”这件事，能删去重复元素。如果我们用之前的方式实现查重，很显然需要查询所有信息，这不是一件好事，时间复杂度是O(n)。而散列表就很适合做这件事了，用hash函数直接映射到下标，可以让我们直接定位到可疑的为止。最理想情况下，时间复杂度一下子就变成O(1)了。所以完全可以用hashmap的方法实现。我们直接忽略val这个字段就可以了。

### 传说中的leetcode1

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        index = dict()
        for i in range(length := len(nums)):
            index.update({nums[i]: i})
        
        for i in range(length):
            if (( t := index.get(target - nums[i], -1)) != -1) and (t != i):
                return [i, t]
```

242：

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        lst = list('abcdefghijklmnopqrstuvwxyz')
        num = [0 for i in range(26)]
        times1 = dict(zip(lst, num))
        times2 = dict(zip(lst, num))
        for i in s:
            times1[i] += 1
        for j in t:
            times2[j] += 1
        for i in times1:
            if not times2[i] == times1[i]:
                return False
        return True
```

### 单词技术

可以专门说一下，Python的collections模块中有一个Counter，可以作字符计数器

## Day 16 二叉树

### 16.1 二叉树

二叉树不单纯是一种数据结构，更是一种常用的算法思维。一切暴力穷举算法，比如 回溯算法、BFS 算法、动态规划 本质上也是把具体问题抽象成树结构。换言之，都有一种”选择分支”的意味。二叉树是一种递归的定义，用根节点和子树组合起来。

满二叉树最好了，深度为h的满二叉树节点数是$2^{n-1}$。完全二叉树相对弱一点，可能没完全排好，完全二叉树是指，二叉树的每一层的节点都紧凑靠左排列，且除了最后一层，其他每层都必须是满的：也就是所有元素序号和位置跟满二叉树相同。也可以说，满二叉树是一种特殊的完全二叉树。另外，完全二叉树的左右子树中，至少有一棵是满二叉树。

英文语境这方面和中文语境不太一样，英文语境的complete binary tree 就是我们说的完全二叉树，处于比较完备的状态。但是full binart tree并不是我们说的满二叉树，而是指所有节点都满足要么没有孩子节点，要么有两个孩子节点的“有即满”的二叉树。向上面那种最完美的满二叉树他们叫perfect binary tree。

### 16.2 其他二叉树分类

#### 二叉搜索树

binary search tree，简称BST，要求对于任何一个节点来说，其左子树的每个节点的值都要小于这个节点的值，右子树的每个节点的值都要大于这个节点的值。你可以简单记为「左小右大」。

Attention！这里说的是比左子树都大，比右子树都小，而不是左孩子右孩子——也就是比左孩子的孩子节点、左孩子的孩子节点的孩子节点都大，比右孩子的孩子节点也要小，比右孩子的孩子的孩子节点也要小。

#### 高度平衡二叉树

它的「每个节点」的左右子树的高度差不超过 1。说白了就是很均衡。

为什么要研究高度平衡二叉树呢？因为我们之前提到，二叉树就像分支。当选择足够好的时候，每一次决策其实就减少了一层树的深度——二叉树相当于提供了一次if-else的选择。假设高度平衡二叉树中共有 N 个节点，那么高度平衡二叉树的高度是O(logN)。这就意味着数据的增删改查效率都会高非常多。

可以想到，如果树的平衡性不好的话，比如所有的节点全堆到上一个节点的左孩子节点位置上，相当于root的左子树深度(n-1)，右子树深度0，达到了极端的不平衡，这种时候相当于失去了if-else的选择性，而是按连接顺序遍历每一个节点——有一种退化成链表的感觉。

#### 自平衡二叉树

如果我们可以在增删二叉树节点时对树的结构进行一些调整，那么就可以让树的高度始终是平衡的，这就是自平衡二叉树。自平衡的二叉树有很多种实现方式，最经典的就是红黑树。

### 16.3 二叉树的遍历（递归遍历 与 层序遍历）

粗略概括的话，二叉树只有递归遍历和层序遍历这两种，再无其他。递归遍历可以衍生出 DFS 算法，层序遍历可以衍生出 BFS 算法。递归遍历二叉树节点的顺序是固定的，但是有三个关键位置，在不同位置插入代码，会产生不同的效果。层序遍历二叉树节点的顺序也是固定的，但是有三种不同的写法，对应不同的场景

主要问题还是在于，之前学的都是线性结构，所以按着顺序后继就可以依次访问所有元素，但是二叉树是非线性结构，所以我们其实说白了就在找一种方式，把二叉树用一条“线”串起来。二叉树的遍历算法主要分为递归遍历和层序遍历两种，都有代码模板。递归代码模板可以延伸出后面要讲的 DFS 算法、回溯算法，层序代码模板可以延伸出后面要讲的 BFS 算法，所以我经常强调二叉树结构的重要性。前序遍历、中序遍历、后序遍历，都属于二叉树的递归遍历，只不过是把自定义代码插入到了代码模板的不同位置而已。

## Day17 递归遍历

### 17.1 递归遍历基础

再强调一下递归，其实说白了就是“把大问题变成一样的小一点的问题，小问题就是一样的更小的问题，直到某一层停下来，总得有个头。然后从这个头慢慢一层一层往上走回去”。

先说递归遍历，其实就是走下去，走到prev和next都是null（走不下去了）就停在这里，也就是“走到头了，该往回了“。所以说递归嘛，就是一个”撞了南墙，终于回头“的过程。

至于前、中、后序遍历说白了只是安排的顺序问题，前就是先根、中就是把根放在中间（左子树和右子树中间）、后就是把根放在最后（左右子树之后）。

> BST的中序遍历结果是有序的

### 多叉树与森林

多叉树结构就是二叉树的一般化，允许一个节点拥有不止一个孩子节点。森林就是多个多叉树的集合（单独一棵多叉树也是一个特殊的森林），用代码表示就是多个多叉树的根节点列表。在并查集算法中，我们会同时持有多棵多叉树的根节点，那么这些根节点的集合就是一个森林。

### 多叉树的递归遍历

唯一的区别是，多叉树没有了中序位置，因为可能有多个节点嘛，所谓的中序位置也就没什么意义了。

## Day18 层序遍历

### 层序遍历基础

二叉树的层序遍历，顾名思义，就是一层一层地遍历二叉树。层序遍历可以借助队列来实现。

### 一点综述

DFS 算法在寻找所有路径的问题中更常用，而 BFS 算法在寻找最短路径的问题中更常用。

### 多叉树的层序遍历

都是用队列来实现，无非就是把二叉树的左右子节点换成了多叉树的所有子节点。所以多叉树的层序遍历也有三种写法，下面一一列举。

## Day19 二叉搜索树

和前面的哈希表、队列这些数据结构不同，树相关的数据结构需要比较强的递归思维，难度会上一个层级。二叉搜索树的性能取决于树的高度，树的高度取决于树的平衡性。

### 19.1 treemap基础 - 二叉搜索树的应用

treemap类似于hashmap，存储键值对，HashMap 底层把键值对存储在一个 table 数组里面，而 TreeMap 底层把键值对存储在一棵二叉搜索树的节点里面。

treemap的Node形如：

```python
class TreeNode:
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
```

首先，get 方法其实就类似上面可视化面板中查找目标节点的操作，根据目标 key 和当前节点的 key 比较，决定往左走还是往右走，可以一次性排除掉一半的节点，复杂度是O(logN)。至于 put, remove, containsKey 方法，其实也是要先利用 get 方法找到目标键所在的节点，然后做一些指针操作，复杂度都是O(logN)。

floorKey, ceilingKey 方法是查找小于等于/大于等于某个键的最大/最小键，这个方法的实现和 get 方法类似，唯一的区别在于，当找不到目标 key 时，get 方法返回空指针，而 ceilingKey, floorKey 方法则返回和目标 key 最接近的键，类似上界和下界。

rangeKeys 方法输入一个 [low, hi] 区间，返回这个区间内的所有键。这个方法的实现也是利用 BST 的性质提高搜索效率：

如果当前节点的 key 小于 low，那么当前节点的整棵左子树都小于 low，根本不用搜索了；如果当前节点的 key 大于 hi，那么当前节点的整棵右子树都大于 hi，也不用搜索了。

firstKey 方法是查找最小键，lastKey 方法是查找最大键，借助 BST 左小右大的特性，非常容易实现。这两个方法比较有意思。其中 selectKey 方法是查找排名为 k 的键（从小到大，从 1 开始），rank 方法是查找目标 key 的排名。

先说 selectKey 方法，一个容易想到的方法是利用 BST 中序遍历结果有序的特性，中序遍历的过程中记录第 k 个遍历到节点，就是排名为 k 的节点。但是这样的时间复杂度是O(k)，因为你至少要用中序遍历经过 k 个节点。一个更巧妙的办法是给二叉树节点中新增更多的字段记录额外信息`int size`，用于记录以当前节点为根的子树的节点总数（包含当前节点）。因为 size 维护的就是当前节点为根的整棵树上有多少个节点，加上 BST 左小右大的特性，那么对于根节点，它只需要查询左子树的节点个数，就知道了自己在以自己为根的这棵树上的排名；知道了自己的排名，就可以确定目标排名的那个节点存在于左子树还是右子树上，从而避免搜索整棵树。

### 19.2 红黑树

红黑树是一种经过优化的能够自平衡的二叉搜索树。任何时候，任何情况下，它的树高都能保持在 O(logN)（完美平衡），这样就能保证增删查改的时间复杂度都是O(logN)。

### 19.3 Huffman树与Huffman编码

这里有贪心算法、动态规划之类的思想。不过咱们这里先只着眼于最浅显的层面。Huffman编码属于无损编码，也就是不会损失信息，可以根据编码从中完全复原出原本的信息。

我们发现一套编码系统中，固长编码是容易随机访问的（因为随便取一个下标，结合一个元素的编码长度，就可以很容易算出来对应下标的元素应该在多长后开始多长后结束），但是固长编码的压缩率有限，也就是有冗余编码；变长编码则可以减少冗余编码，但是不适合随机访问。

Huffman方法是很优秀的编码，相应的量化公式要用信息论中的信息熵等概念证明，也不在当前的考虑范围当中。

> 可变长度编码有“不应存在编码A，是编码B的前缀”的原则。
> 这样要么会无法保证编码的唯一性（这个应该有很多例子）、要么会大幅度增加解码的时间复杂度（如A:1, B:100, C:1000这种编码方式，每次看到1都要往后扫描，解码复杂度从O(N)上升到O(NK)。这里的N是编码后长度，K是最长的编码长度）

每次取走两个最小概率的节点作为一组，并合成一个新子树（其中概率大的作为左孩子，概率小的作为右孩子）。他们的双亲节点放回原来的所有节点中。重复这个过程，直到全都合成一颗哈夫曼树。之后给所有靠左的边都写一个0，靠右的都写一个1。用这棵树生成编码，即为哈夫曼编码。

这里其实严谨的说法是带权无向图。用叶子节点的值（通常为一个符号的出现频数或概率之类）乘以从根节点到该叶子节点的路径长度，最后对所有叶子节点求和，这就是 树的带权路径长度（Weighted Path Length），简称 WPL。（路径长度即为编码长度）

用二进制编码本身具有二分性（0和1二分），所以每次选择一个0/1中的一个就是做一次选择。在选择过程中，我们希望越常见的越靠上层（也就是深度越小，越容易定下来）。所以我们让概率越大的越最后被融入。

## Day22 动态规划

### 22.1 最优子结构性质

动态规划包括`最优子结构`、`无后效性`、`重复子问题`三个性质。

- 最优子结构
  - 其核心定义为问题的最优解包含子问题的最优解，即原问题的最优解可通过子问题的最优解合并得到。也就是可以通过前面推出来的东西进一步推导后一步的结构
- 无后效性
  - 在推导后面阶段的状态过程中，我们只关心后面发生的过程，前面已经发生的过程不会产生影响。
- 重复子问题
  - 在拆解一个大问题的过程中，不同的问题可能会导向一个相同的子问题。这个性质有时候也叫重叠子问题。

### 22.2 带备忘录的递推 - 自底而上的动态规划

所以很多时候我们可以用带记忆功能，加了备忘录的程序处理这类问题。我们仍然用斐波那契数列举例：

用这个方式就能很直观进行对比了：

```python
from collections import deque
from time import time

def fibs(n: int, memory: deque = [2, 1, 1]):
    if n in {1, 2}:
        return 1
    if len(memory) < 3:
        memory.clear()
        for i in [2, 1, 1]:
            memory.append(i)
    if n <= memory[0]:
        return memory[n]
    i = memory[0]
    while (i < n):
        memory.append(memory[i] + memory[i-1])
        i+=1
        memory[0] += 1
    return memory[-1]

def basic_method(n: int):
    if n in {1, 2}:
        return 1
    return basic_method(n - 1) + basic_method(n - 2)

if __name__ == '__main__':
    time1 = time()
    lst = deque()
    lst.appendleft(0) # 第一位元素用来记录当前已经生成到第几项
    print(fibs(40, memory=lst))
    time2 = time()
    # print(list(lst))
    print(f"Totally cost :{time2 - time1}")

    time3 = time()
    print(basic_method(45))
    time4 = time()
    print(f"Totally cost {time4 - time3}")
```

用这种方法得到的是算法是监督是O(N)，已经比起原来的指数级时间复杂度效率搞了太多太多了。

这种规划方式是自底而上的，从低级子问题向上级子问题推导，利用低级子问题给出上级子问题的结果，直到达到最上层，也就得到了我们想要的结果。

### 22.3 带备忘录的递归 - 自上而下的动态规划

我们仍然需要提供一个备忘录，每次遇到新的结构就记录下来，这样以后再用到也就不用反复查询了。这样子自上而下的动态规划和上面自下而上的动态规划是等价的，可以互相等价。这就是为什么我们可以看到两种不同的写法都自称动态规划。

递归写法如：

```python
def fibs_another(n: int, memory: list):
    # 通常使用hashmap实现查询功能，不过这里的项数和索引显然有很好的对应关系
    # 所以我们干脆用list简化一下
    if len(memory) < n:
        for i in range(n):
            memory.append(None)
    if n in {1, 2}:
        return 1
    else:
        if (t:=memory[n-1]) is not None:
            return t
        memory[n-1] = fibs_another(n-1, memory=memory) + fibs_another(n-2, memory=memory)
        return memory[n-1]
```

用C语言：

```c
int get(int n, int* stack) {
        switch (n) {
            case 0: return 0;
            case 1: return 1;
            default:
                if (stack[n]!= 0) return stack[n];
                stack[n] = get(n-1, stack) + get(n-2, stack);
                return stack[n];
        }
}

int fib(int n) {
    if (n == 0 || n == 1) return n;
    int *stack = (int *) calloc(n+1, sizeof(int));
    stack[0] = 0;
    stack[1] = 1;
    return get(n, stack);
}
```

### 22.4 状态转移方程

就像上面的斐波那契的公式，f(n) 的函数参数会不断变化，所以你把参数 n 想做一个状态，这个状态 n 是由状态 n - 1 和状态 n - 2 转移（相加）而来，这就叫状态转移。对备忘录或 DP table 的初始化操作，都是围绕这个方程式的不同表现形式。很容易发现，其实状态转移方程直接代表着暴力解法。千万不要看不起暴力解，动态规划问题最困难的就是写出这个暴力解，即状态转移方程。只要写出暴力解，优化方法无非是用备忘录或者 DP table。

所以，我们需要把握住：

- 确定「状态」，也就是原问题和子问题中会变化的变量
- 确定「选择」，也就是导致「状态」产生变化的行为
- 明确 dp 函数/数组的定义。我们这里讲的是自顶向下的解法，所以会有一个递归的 dp 函数，一般来说函数的参数就是状态转移中会变化的量，也就是上面说到的「状态」；函数的返回值就是题目要求我们计算的量

### 22.5 技巧1 - 借助数学归纳思想实现

我们用LIS为例，Longest Increasing Subsequence最长递增子序列。

> 给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。
> 子序列 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。
> 例如，输入nums = [10,9,2,5,3,7,101,18]，得到4

**相信大家对数学归纳法都不陌生，高中就学过，而且思路很简单。比如我们想证明一个数学结论，那么我们先假设这个结论在 k < n 时成立，然后根据这个假设，想办法推导证明出 k = n 的时候此结论也成立。如果能够证明出来，那么就说明这个结论对于 k 等于任何数都成立。类似的，我们设计动态规划算法，不是需要一个 dp 数组吗？我们可以假设 dp[0...i-1] 都已经被算出来了，然后问自己：怎么通过这些结果算出 dp[i]？**

所以实际上，动态规划的最优子结构性质和无后效性就保证了求解问题过程中，前面的结果是可复用的，我们可以一直使用前面的性质。正是因为这一优良性质，才保证了只需要建立一个备忘录或者说DP table，就可以完成整个程序。

> 给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。
> 子序列 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。

我们来分析一下这个问题。首先我们要知道状态转移是怎么转移的。在这道题中，可以是对于一个list[n-1] 变化到list[n]。我们在一个序列后添加一个字符，从最大子序列的角度考虑，如果他产生了影响，那肯定是连接在某个序列之后了。如果它在任何地方都连接不上，那就是单独成一个新的子序列[a]，长度为1.所以我们确认了变换过程中的状态：以nums[i]结尾的最大子序列长度。（考虑角度还是，知道前n-1项后怎么求第n项）。顺着这个思路，就顺手推舟了。

很显然，这个过程里面自下而上写会方便一点。

## Day24 贪心算法

有些问题其实不需要完整地穷举所有可行解，就可以推导出最优解。这样一来，进一步减少了穷举空间，效率自然会更高。即：勇敢梭哈，试图一次走到头。对于当前的计算机而言，一切算法都是穷举，所以贪心算法在做的，就是选择当前来看最稳定的决策，从而实现剪枝。

贪心算法和动态规划都常用于解决优化问题。它们之间存在一些相似之处，比如都依赖最优子结构性质，但工作原理不同。

首先我们复习一下最优子结构性质：

> 指一个问题的最优解包含其子问题的最优解，这一性质是动态规划和贪心算法的基础
> 其核心定义为问题的最优解包含子问题的最优解，即原问题的最优解可通过子问题的最优解合并得到。

- 动态规划会根据之前阶段的所有决策来考虑当前决策，并使用过去子问题的解来构建当前子问题的解。
- 贪心算法不会考虑过去的决策，而是一路向前地进行贪心选择，不断缩小问题范围，直至问题被解决。

### 24.1 贪心选择性质

贪心选择性质就是说能够通过局部最优解直接推导出全局最优解。我们用找零问题举例。

现在有5元、2元、1元的纸币。如果要找零11元，要怎么做？ 大多数情况下，我们肯定希望找零过程尽可能方便——时间快，数量少。所以，从纸币数量最少的角度考虑，当然是选5元、5元、1元的组合。为什么是两张5元一张1元？因为我们要尽量快地逼近结果，所以我们贪婪的选每一次的局部最优解，最终推出了全局最优解。这就是所谓的贪心选择性质，局部最优解组合起来就是全局最优解。

## Day27 堆

### 27.1 二叉堆

二叉堆是一种特殊的二叉树，这棵二叉树上的任意节点的值，都必须大于等于（或小于等于）其左右子树所有节点的值。如果是大于等于，我们称之为「大顶堆」，如果是小于等于，我们称之为「小顶堆」。

二叉堆就是一种能够动态排序的数据结构。所谓动态排序，就是说我们可以不断往数据结构里面添加或删除元素，数据结构会自动调整元素的位置，使得我们可以有序地从数据结构中读取元素，这是一般的排序算法做不到的。能动态排序的常用数据结构其实只有两个，一个是优先级队列（底层用二叉堆实现），另一个是二叉搜索树。二叉搜索树的用途更广泛，优先级队列能做的事情，二叉搜索树其实都能做。但优先级队列的 API 和代码实现相较于二叉搜索树更简单，所以一般能用优先级队列解决的问题，我们没必要用二叉搜索树。

优先级队列其实就是二叉堆的一种应用。例如最大堆，权重最大的值先出来，这就像是队列，所以叫优先级队列。虽然它的 API 像队列，但它的底层原理和二叉树有关，和队列没啥关系。

在之前的所有内容中，我都把二叉堆作为一种二叉树来讲解。但实际上，我们在代码实现的时候，不会用类似 HeapNode 的节点类来实现，而是用数组来模拟二叉树结构。

### 27.2 二叉堆的代码实现

### 27.3 线段树

线段树可以在 O(logN) 的时间复杂度查询任意长度的区间元素聚合值，在 O(logN) 的时间复杂度对任意长度的区间元素进行动态修改，其中 N 为数组中的元素个数。线段树其实就是把一个区间分成若干小区间，相当于把一整条线段拆成小线段，也实现了”剪纸“的”选择“的操作。

前缀和技巧有它的局限性，即 nums 数组本身不能变化。一旦 nums[i] 变化了，那么 suffixMin[0..i] 的值都会失效，需要 O(N) 的时间复杂度重新计算 suffixMin 数组。对于这种希望对整个区间进行查询，同时支持动态修改元素的场景，是线段树结构的应用场景。

## Day28 字典树

### 28.1 trie树

是一种针对字符串进行特殊优化的数据结构，在处理字符串相关操作时有诸多优势，比如节省公共字符串前缀的内存空间、方便处理前缀操作、支持通配符匹配等。

一句话概括，字典树的关键就是”让每一次选择更有意义“，每一个节点不再是单纯的序号，而是具体的某个字符。比如but后的节点第0个孩子对应a，第1个对应b之类，那么but后选0个节点-25个节点就意味着字符串是buta-butz。这就是前缀树，有prefix的味道，是不是很适合做代码补全？
