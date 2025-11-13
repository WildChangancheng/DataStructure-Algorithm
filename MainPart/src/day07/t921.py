from collections import deque
class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        q = deque()
        pointer = 0
        for i in s:
            if i == '(':
                q.append('(')
                pointer += 1
                continue
            else:
                if pointer == 0 or q[pointer-1]==')':
                    q.append(')')
                    pointer += 1
                    continue
                else:
                    q.pop()
                    pointer -= 1
        return pointer
        