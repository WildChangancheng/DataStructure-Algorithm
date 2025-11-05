from time import perf_counter
from random import sample, shuffle


def deal_pivot_key(lst: list[int], low: int, high: int):
    pivot_key = lst[low]

    while low < high:
        while (low < high) and (lst[high] >= pivot_key):
            high -= 1
            # 保证high不会比low更低
            # 一直降high的位置，如果这层while被打破，就意味着位于high的元素比pivot_key更小，需要交换

        lst[low], lst[high] = lst[high], lst[low]
        # 更换high和low，这里的low相当于pivot_key
        # 交换以后，现在带pivot_key位于high位置

        while (low < high) and (lst[low] <= pivot_key):
            low += 1

        lst[low], lst[high] = lst[high], lst[low]
        # 如果再交换，就把pivot_key换到新的low位置
    
    return low


def quick_sort(lst: list[int], low: int, high: int):
    if low < high:
        pivot = deal_pivot_key(lst, low, high) # 这样返回的就是那个调整好的pivot
        quick_sort(lst, low, pivot-1)
        quick_sort(lst, pivot+1, high)

    return 


def start(lst: list[int]):
    quick_sort(lst, 0, len(lst)-1)
    return lst


def test_sort(fun): 
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
        (sample(range(1000), 10), None),               # 随机50个
        (sample(range(1000), 15), None),               # 随机50个
        (sample(range(1000), 20), None),               # 随机50个
        (sample(range(1000), 25), None),               # 随机50个
        (sample(range(1000), 50), None),               # 随机50个
        (list(range(100, 0, -1)), list(range(1, 101))),       # 100个逆序
        (sample(range(10000), 100), None),
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
    test_sort(fun = start)


