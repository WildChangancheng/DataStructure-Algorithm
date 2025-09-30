from time import perf_counter
from random import sample


def bubble_sort(input_lst: list):
    n = len(input_lst)
    for i in range(1, n)[::-1]:
        for j in range(0, i):
            if input_lst[j+1] < input_lst[j]:
                input_lst[j], input_lst[j+1] = input_lst[j+1], input_lst[j]
    return input_lst


def bubble_sort_version1(input_lst: list):
    n = len(input_lst)
    for i in range(1, n)[::-1]:
        flag = True
        for j in range(0, i):
            if input_lst[j+1] < input_lst[j]:
                input_lst[j], input_lst[j+1] = input_lst[j+1], input_lst[j]
            flag = False
        if flag:
            break
    return input_lst


def bubble_sort_version2_wrong(input_lst: list):
    n = len(input_lst)
    for i in range(1, n)[::-1]:
        for j in range(0, i):
            if input_lst[j+1] < input_lst[j]:
                input_lst[j], input_lst[j+1] = input_lst[j+1], input_lst[j]
                n = j
    return input_lst
# 这是错误的写法，因为最后更新的升级位置是j。但是for循环之后每次都还是执行所有代码
# 请自行思考

# 答案是：for i in range(1, n)[::-1] 
# 在循环开始时就把要迭代的序列确定好了
# 后面再修改 n 并不会改变这个序列
# 所以 n = j 并不能缩小外层 for 的范围——你的“优化”在当前写法下是无效的


def bubble_sort_version2(input_lst: list):
    n = len(input_lst)
    while n > 1:
        last_change = 0
        for j in range(0, n-1):
            if input_lst[j] > input_lst[j+1]:
                input_lst[j], input_lst[j+1] = input_lst[j+1], input_lst[j]
                last_change = j + 1    # 注意是 j+1（下一轮只需到 new_n-1）
            n = last_change
    return input_lst


def test_bubble_sort(fun): 
    """带计时功能的冒泡排序测试"""
    test_cases = [
        ([], []),                               # 空列表
        ([1], [1]),                             # 单元素
        ([2, 1], [1, 2]),                       # 两个元素
        ([5, 3, 8, 4, 2], sorted([5, 3, 8, 4, 2])), # 普通乱序
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),     # 已经有序
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),     # 完全逆序
        ([7, 7, 7, 7, 7], [7, 7, 7, 7, 7]),     # 全部重复
        ([3, 1, 2, 3, 1, 2], sorted([3, 1, 2, 3, 1, 2])), # 部分重复
        ([0, -1, 5, -3, 8, 2], sorted([0, -1, 5, -3, 8, 2])), # 包含负数
        (list(range(100, 0, -1)), list(range(1, 101))),       # 100个逆序
        (sample(range(1000), 50), None),               # 随机50个
        (sample(range(10000), 200), None),
    ]

    print(f"\n———————————— Test : {fun.__name__} ————————————")
    for i, (input_lst, expected) in enumerate(test_cases):
        start = perf_counter()   # 高精度计时
        result = fun(input_lst.copy())
        end = perf_counter()
        elapsed = (end - start) * 1000  # 转换为毫秒

        if expected is None:
            expected = sorted(input_lst)
            # 这是用内置的sorted做验证
        print(f"Test {i+1}: {result} == {expected} -> {result == expected} "
              f"(耗时 {elapsed:.3f} ms)")
if __name__ == '__main__':
    test_bubble_sort(fun = bubble_sort)
    test_bubble_sort(fun = bubble_sort_version1)
    test_bubble_sort(fun = bubble_sort_version2)