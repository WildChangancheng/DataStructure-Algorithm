from typing import List

class Solution:
    def set_memory(self, n: int) -> None:
        self.memory = [1 for _ in range(n)]

    def calculate(self, index: int, nums: List[int]) -> int:
        if self.memory[index] != 1:
            return self.memory[index]

        tmp = 1
        for i in range(index):
            if nums[index] > nums[i]:
                tmp = max(tmp, self.memory[i] + 1)
        self.memory[index] = tmp
        return tmp

    def lengthOfLIS(self, nums: List[int]) -> int:
        length = len(nums)
        if length == 0:
            return 0
        self.set_memory(length)
        for i in range(length):
            self.calculate(i, nums)
        return max(self.memory)
