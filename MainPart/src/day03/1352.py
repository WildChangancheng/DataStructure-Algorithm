class ProductOfNumbers:

    def __init__(self):
        self.prefix = [1]  # 前缀积列表

    def add(self, num: int) -> None:
        if num == 0:
            # 重置前缀积（0 之后的积重新算）
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):
            return 0  # 表示包含了某个 0
        return self.prefix[-1] // self.prefix[-1 - k]
    


# Your ProductOfNumbers object will be instantiated and called as such:
# obj = ProductOfNumbers()
# obj.add(num)
# param_2 = obj.getProduct(k)