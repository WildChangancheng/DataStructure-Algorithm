from typing import List

class Solution:
    def set_memory(self, n: int) -> None:
        self.memory = [None for i in range(n)]
    def calculate(self, index: int, nums: List[int]) -> int:
        if index == 0:
            self.memory[0] = 1
            return 1
        tmp = 1
        for i in range(index + 1):
            if (nums[index] >= nums[i]):
                if ((new_sum := self.memory[i] + 1)> tmp):
                    tmp = new_sum
        self.memory[index] = tmp
        return tmp

    def lengthOfLIS(self, nums: List[int]) -> int:
        length = len(nums)
        self.set_memory(length)
        self.calculate(index=length-1, nums=nums)
        