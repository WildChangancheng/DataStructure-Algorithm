from collections import deque
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        lst = deque()
        node = head
        while not (node.next is None):
            lst.append(node)
            node = node.next
        lst.append(node)
        n = len(lst)
        pointer1 = 0
        pointer2 = n - 1
        result = deque()
        while (pointer2 > pointer1):
            result.append(lst[pointer1])
            result.append(lst[pointer2])
            pointer1 += 1
            pointer2 -= 1
        if pointer1 == pointer2:
            result.append(lst[pointer1])
        for i in range(n-1):
            result[i].next = result[i+1]
        result[n-1].next = None
        head = result[0]