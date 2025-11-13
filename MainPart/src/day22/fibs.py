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
    lst = [1, 1]
    print(fibs_another(40, memory=lst))
    time4 = time()
    print(f"Totally cost :{time4 - time3}")


    time5 = time()
    print(basic_method(40))
    time6 = time()
    print(f"Totally cost {time6 - time5}")