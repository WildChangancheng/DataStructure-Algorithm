# note

## 0 前言

考虑到课程乱七八糟，难度不平滑等问题，特此增设基础算法分支。该分支难度低，内容浅显易懂，作为课程正篇的前置内容，辅助学习。

这里用Python和C语言双实现。

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
