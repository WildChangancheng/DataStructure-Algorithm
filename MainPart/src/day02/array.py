class MyArray:
    def __init__(self, init_capacity: int = 1):
        self.data = [None for i in range(init_capacity)]
        self.size = 0

    def append(self, e):
        capacity = len(self.data)
        if self.size == capacity:
            self._resize(2 * capacity)
        self.data[self.size] = e
        self.size += 1
        return 

    def add(self, index, e):
        # 检查索引越界
        self._check_position_index(index)

        cap = len(self.data)
        # 看 data 数组容量够不够
        if self.size == cap:
            self._resize(2 * cap)

        # 搬移数据 data[index..] -> data[index+1..]
        # 给新元素腾出位置
        for i in range(self.size-1, index-1, -1):
            self.data[i+1] = self.data[i]
        
        # 插入新元素
        self.data[index] = e

        self.size += 1

    def add_first(self, e):
        self.add(0, e)

    # 删
    def remove_last(self):
        if self.size == 0:
            raise Exception("NoSuchElementException")
        cap = len(self.data)
        # 可以缩容，节约空间
        if self.size == cap // 4:
            self._resize(cap // 2)

        deleted_val = self.data[self.size - 1]
        # 删除最后一个元素
        self.data[self.size - 1] = None
        self.size -= 1

        return deleted_val

    def remove(self, index):
        # 检查索引越界
        self._check_element_index(index)

        cap = len(self.data)
        # 可以缩容，节约空间
        if self.size == cap // 4:
            self._resize(cap // 2)

        deleted_val = self.data[index]

        # 搬移数据 data[index+1..] -> data[index..]
        for i in range(index + 1, self.size):
            self.data[i - 1] = self.data[i]

        self.data[self.size - 1] = None
        self.size -= 1

        return deleted_val

    def remove_first(self):
        return self.remove(0)

    # 查
    def get(self, index):
        # 检查索引越界
        self._check_element_index(index)

        return self.data[index]

    # 改
    def set(self, index, element):
        # 检查索引越界
        self._check_element_index(index)
        # 修改数据
        old_val = self.data[index]
        self.data[index] = element
        return old_val

    # 工具方法
    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    # 将 data 的容量改为 newCap
    def _resize(self, new_cap):
        temp = [None] * new_cap
        for i in range(self.size):
            temp[i] = self.data[i]
        self.data = temp

    def _is_element_index(self, index):
        return 0 <= index < self.size

    def _is_position_index(self, index):
        return 0 <= index <= self.size

    def _check_element_index(self, index):
        if not self._is_element_index(index):
            raise IndexError(f"Index: {index}, Size: {self.size}")

    def _check_position_index(self, index):
        if not self._is_position_index(index):
            raise IndexError(f"Index: {index}, Size: {self.size}")

    def display(self):
        print(f"size = {self.size}, cap = {len(self.data)}")
        print(self.data)


# Usage example
if __name__ == "__main__":
    arr = MyArray(init_capacity=3)

    # 添加 5 个元素
    for i in range(1, 6):
        arr.append(i)

    arr.remove(3)
    arr.add(1, 9)
    arr.add_first(100)
    val = arr.remove_last()

    # 100 1 9 2 3
    for i in range(arr.get_size()):
        print(arr.get(i))