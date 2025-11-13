# LeetCode 707
#  Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)
class Node:
    def __init__(self, val, next = None, prev = None):
        self.val = val
        self.next = next
        self.prev = prev

class MyLinkedList:
    def __init__(self):
        self.virtual_head = Node(val = None, next = None, prev = None)
        self.virtual_tail = Node(val = None, next = None, prev = None)
        self.virtual_head.next = self.virtual_tail
        self.virtual_tail.prev = self.virtual_head
        self.length = 0
    
    def __is_valid_to_insert(self, index: int) -> bool:
        return (index >= 0) and (index <= self.length)
    def __is_valid_to_delete(self, index: int) -> bool:
        return (index >= 0) and (index < self.length)
    
    def get_node(self, index: int) -> Node:
        if not self.__is_valid_to_delete(index=index):
            return -1
        next = self.virtual_head
        for i in range(index+1):
            next = next.next
        return next
    
    def get(self, index: int) -> int:
        return self.get_node(index).val

    def addAtHead(self, val: int) -> None:
        # 这是原始的写法1
        node = Node(val = val, next = self.virtual_head.next, prev = self.virtual_head)
        self.virtual_head.next.prev = node
        self.virtual_head.next = node
        self.length += 1
        

    def addAtTail(self, val: int) -> None:
        # 这是原始的写法1
        node = Node(val = val, next = self.virtual_tail, prev = self.virtual_tail.prev)
        self.virtual_tail.prev.next = node
        self.virtual_tail.prev = node
        self.length += 1
        

    def addAtIndex(self, index: int, val: int) -> None:
        if not self.__is_valid_to_insert(index=index):
            return
        prev_node = self.virtual_head if index == 0 else self.get_node(index - 1)
        next_node = prev_node.next
        cur_node = Node(val = val, prev = prev_node, next = next_node)
        prev_node.next, next_node.prev = cur_node, cur_node
        self.length += 1
        

    def deleteAtIndex(self, index: int) -> None:
        if not self.__is_valid_to_delete(index=index):
            return
        prev_node = self.virtual_head if index == 0 else self.get_node(index - 1)
        next_node = prev_node.next.next
        prev_node.next, next_node.prev = next_node, prev_node
        self.length -= 1

