from typing import List

class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.sum_array = [0] + [sum(nums[0:i+1:1]) for i in range(len(nums))]
        

    def sumRange(self, left: int, right: int) -> int:
        return self.sum_array[right] - self.sum_array[left]        


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)