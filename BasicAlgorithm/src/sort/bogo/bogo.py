from time import perf_counter
from random import sample, shuffle


def bogo_sort(lst):
    if lst == []:
        return []
    def __is_sorted(output: list):
        tmp = output[0]
        for i in output:
            if tmp <= i:
                tmp = i
                continue
            return  False
        return True
    while not __is_sorted(lst):
        shuffle(lst)
    return lst



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
    test_bubble_sort(fun = bogo_sort)
