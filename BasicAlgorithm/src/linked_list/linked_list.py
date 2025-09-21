from typing import Any
class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None
    def __is_valid_index(self, index: int) -> bool:
        return ((index >= 0) and (index < self.size))
    def __node_from_data(self, data: Any) -> Node:
        return Node(data=data)
    def get_node_with_index(self, index: int) -> Node:
        current_node: Node = self.head
        for _ in range(index):
            current_node = current_node.next
        return current_node
    def insert(self, data: Any, index: int) -> None:
        node = self.__node_from_data(data=data)
        if self.size == 0:
            self.head = node
            self.tail = node
            self.size = 1
        elif index == self.size:
            self.tail.next = node
            self.tail = node
            self.size += 1
        elif not self.__is_valid_index(index):
            raise IndexError("Index out of range")
        elif index == 0:
            node.next = self.head
            self.head = node
            self.size += 1
        else:
            pre_node = self.get_node_with_index(index-1)
            node.next = pre_node.next
            pre_node.next = node
            self.size += 1
    def delete(self, index: int)->None:
        if not self.__is_valid_index(index=index):
            raise IndexError("Index out of range")
        elif index == 0:
            node = self.head
            self.head = node.next
            self.size -= 1
            del node
        elif index == self.size - 1:
            node = self.tail
            self.tail = self.get_node_with_index(index=index-1)
            self.tail.next = None
            self.size -= 1
            del node
        else:
            pre:    Node = self.get_node_with_index(index=index)
            node:   Node = pre.next
            sub:    Node = node.next
            pre.next = sub
            self.size -= 1
            del node
    def show(self) -> None:
        current_node = self.head
        while current_node is not None:
            print(f"{current_node.data}", end='')
            if current_node.next is not None:
                print(" -> ", end='')
            current_node = current_node.next
        print("") 



def test_linked_list():
    print("=" * 50)
    print("开始测试链表实现")
    print("=" * 50)
    
    # 测试1: 创建空链表
    print("\n1. 测试空链表:")
    ll = LinkedList()
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出空行
    
    # 测试2: 插入第一个元素
    print("\n2. 测试插入第一个元素:")
    ll.insert(10, 0)
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 10
    
    # 测试3: 在末尾插入元素
    print("\n3. 测试在末尾插入:")
    ll.insert(20, 1)
    ll.insert(30, 2)
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 10 -> 20 -> 30
    
    # 测试4: 在头部插入元素
    print("\n4. 测试在头部插入:")
    ll.insert(5, 0)
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 5 -> 10 -> 20 -> 30
    
    # 测试5: 在中间插入元素
    print("\n5. 测试在中间插入:")
    ll.insert(15, 2)
    ll.insert(25, 4)
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 5 -> 10 -> 15 -> 20 -> 25 -> 30
    
    # 测试6: 删除头部元素
    print("\n6. 测试删除头部:")
    ll.delete(0)
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 10 -> 15 -> 20 -> 25 -> 30
    
    # 测试7: 删除尾部元素
    print("\n7. 测试删除尾部:")
    ll.delete(4)  # 现在size=5，索引4是最后一个
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 10 -> 15 -> 20 -> 25
    
    # 测试8: 删除中间元素
    print("\n8. 测试删除中间:")
    ll.delete(1)
    print(f"链表大小: {ll.size}")
    ll.show()  # 应该输出: 10 -> 20 -> 25
    
    # 测试9: 边界情况测试 - 删除最后一个元素
    print("\n9. 测试删除最后一个元素:")
    ll2 = LinkedList()
    ll2.insert(100, 0)
    ll2.delete(0)
    print(f"链表大小: {ll2.size}")
    ll2.show()  # 应该输出空行
    print(f"head: {ll2.head}, tail: {ll2.tail}")  # 都应该为None
    
    # 测试10: 异常情况测试 - 索引越界
    print("\n10. 测试异常情况:")
    try:
        ll.insert(999, 10)  # 索引越界
        print("❌ 应该抛出异常但没有抛出")
    except IndexError as e:
        print(f"✅ 正确抛出异常: {e}")
    
    try:
        ll.delete(10)  # 索引越界
        print("❌ 应该抛出异常但没有抛出")
    except IndexError as e:
        print(f"✅ 正确抛出异常: {e}")
    
    try:
        ll.delete(-1)  # 负索引
        print("❌ 应该抛出异常但没有抛出")
    except IndexError as e:
        print(f"✅ 正确抛出异常: {e}")
    
    # 测试11: 复杂操作序列
    print("\n11. 测试复杂操作序列:")
    ll3 = LinkedList()
    # 插入多个元素
    for i in range(5):
        ll3.insert(i * 10, i)
    print("初始链表:")
    ll3.show()  # 0 -> 10 -> 20 -> 30 -> 40
    
    # 混合插入删除
    ll3.delete(2)  # 删除20
    ll3.insert(25, 2)  # 在位置2插入25
    ll3.insert(5, 0)  # 在头部插入5
    ll3.delete(4)  # 删除30
    ll3.insert(35, 4)  # 在末尾插入35
    
    print("操作后链表:")
    ll3.show()  # 应该输出: 5 -> 0 -> 10 -> 25 -> 35
    
    # 测试12: 验证链表连接正确性
    print("\n12. 验证链表连接正确性:")
    current = ll3.head
    print("遍历链表:")
    while current:
        print(f"节点数据: {current.data}, 下一个节点: {current.next.data if current.next else None}")
        current = current.next
    
    print("=" * 50)
    print("测试完成!")
    print("=" * 50)


if __name__ == '__main__':
    link = LinkedList()
    link.insert(data=1, index=0)  # 1
    link.insert(data=2, index=1)  # 1 -> 2
    link.insert(data=4, index=2)  # 1 -> 2 -> 4
    link.insert(data=3, index=2)  # 1 -> 2 -> 3 -> 4
    link.show()  # 输出: 1 -> 2 -> 3 -> 4

    test_linked_list()