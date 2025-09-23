from pprint import pprint

class Stack:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity: int = capacity
        self.bottom_index: int = 0
        self.top_index: int = -1
        self.content: list = [None for i in range(capacity)]
    
    def __is_not_full(self) -> bool:
        return (self.top_index + 1) < self.capacity  # 修正：应该是 self.capacity
    
    def show(self) -> None:
        tmp = [str(i) if i is not None else "None" for i in self.content]  # 修正：self.content
        tmp[self.bottom_index] += " (bottom)"  # 修正：self.bottom_index
        if self.top_index >= 0:  # 添加边界检查
            tmp[self.top_index] += " (top)"
        pprint(tmp)
    
    def pop(self):
        if self.top_index < 0:  # 添加空栈检查
            raise IndexError("Pop from empty stack")
        data = self.content[self.top_index]
        self.content[self.top_index] = None  # 清空位置
        self.top_index -= 1
        return data
    
    def push(self, data) -> None:
        if not self.__is_not_full():
            raise IndexError("Stack is full")
        self.top_index += 1
        self.content[self.top_index] = data

def test_stack():
    print("=" * 50)
    print("Testing Stack Implementation")
    print("=" * 50)
    
    # Test 1: Create stack with valid capacity
    print("\n1. Testing stack creation:")
    try:
        stack = Stack(5)
        print(f"✅ Stack created with capacity: {stack.capacity}")
        print(f"   Top index: {stack.top_index}, Bottom index: {stack.bottom_index}")
    except Exception as e:
        print(f"❌ Failed to create stack: {e}")
    
    # Test 2: Create stack with invalid capacity
    print("\n2. Testing invalid capacity:")
    try:
        invalid_stack = Stack(0)
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Test 3: Push elements
    print("\n3. Testing push operations:")
    try:
        stack = Stack(3)
        stack.push(10)
        stack.push(20)
        stack.push(30)
        print("✅ Successfully pushed 3 elements")
        stack.show()
    except Exception as e:
        print(f"❌ Push failed: {e}")
    
    # Test 4: Push to full stack
    print("\n4. Testing push to full stack:")
    try:
        stack.push(40)  # This should fail
        print("❌ Should have raised IndexError")
    except IndexError as e:
        print(f"✅ Correctly raised IndexError: {e}")
    
    # Test 5: Pop elements
    print("\n5. Testing pop operations:")
    try:
        stack = Stack(3)
        stack.push(100)
        stack.push(200)
        stack.push(300)
        
        print("Before popping:")
        stack.show()
        
        popped = stack.pop()
        print(f"✅ Popped element: {popped}")
        
        popped = stack.pop()
        print(f"✅ Popped element: {popped}")
        
        print("After popping twice:")
        stack.show()
    except Exception as e:
        print(f"❌ Pop failed: {e}")
    
    # Test 6: Pop from empty stack
    print("\n6. Testing pop from empty stack:")
    try:
        stack = Stack(2)
        stack.push(1)
        stack.pop()
        stack.pop()  # This should fail
        print("❌ Should have raised IndexError")
    except IndexError as e:
        print(f"✅ Correctly raised IndexError: {e}")
    
    # Test 7: Mixed operations
    print("\n7. Testing mixed operations:")
    try:
        stack = Stack(4)
        stack.push('A')
        stack.push('B')
        popped1 = stack.pop()
        stack.push('C')
        stack.push('D')
        popped2 = stack.pop()
        stack.push('E')
        
        print(f"✅ Popped: {popped1}, {popped2}")
        print("Final stack:")
        stack.show()
    except Exception as e:
        print(f"❌ Mixed operations failed: {e}")
    
    # Test 8: Test stack full detection
    print("\n8. Testing stack full detection:")
    try:
        stack = Stack(2)
        stack.push(1)
        stack.push(2)
        print(f"✅ Stack is full: {not stack._Stack__is_not_full()}")  # Accessing private method for testing
    except Exception as e:
        print(f"❌ Full detection failed: {e}")
    
    # Test 9: Test stack empty state
    print("\n9. Testing stack empty state:")
    try:
        stack = Stack(2)
        print(f"✅ Stack is empty: {stack.top_index == -1}")
        stack.push(1)
        stack.pop()
        print(f"✅ Stack is empty after pop: {stack.top_index == -1}")
    except Exception as e:
        print(f"❌ Empty state test failed: {e}")
    
    # Test 10: Boundary values
    print("\n10. Testing boundary values:")
    try:
        stack = Stack(1)  # Minimum valid capacity
        stack.push("single")
        print("✅ Single-element stack works")
        stack.show()
        popped = stack.pop()
        print(f"✅ Popped from single-element stack: {popped}")
    except Exception as e:
        print(f"❌ Boundary test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Testing completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_stack()