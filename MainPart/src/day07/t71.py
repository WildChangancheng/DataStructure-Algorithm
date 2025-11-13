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
        