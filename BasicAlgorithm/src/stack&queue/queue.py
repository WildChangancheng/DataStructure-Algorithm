class Queue:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.front = 0
        self.rear = 0
        self.capacity = capacity
        self.size = 0
        self.content = [None for i in range(capacity)]
    
    def show(self):
        tmp = []
        for i in range(self.capacity):
            element = self.content[i]
            tags = []
            if i == self.front and self.size > 0:
                tags.append("(front)")
            if i == self.rear:
                tags.append("(rear)")
            if element is not None:
                tmp.append(f"{element}{''.join(tags)}")
            else:
                tmp.append(f"None{''.join(tags)}")
        print("Queue: [" + " | ".join(tmp) + "]")
        print(f"Size: {self.size}, Front: {self.front}, Rear: {self.rear}")
    
    def __is_not_full(self) -> bool:
        return self.size < self.capacity
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def enqueue(self, element):
        if not self.__is_not_full():
            raise ValueError("Queue is full")
        self.content[self.rear] = element
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise ValueError("Queue is empty")
        element = self.content[self.front]
        self.content[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return element

def test_queue():
    print("=" * 60)
    print("Testing Queue Implementation")
    print("=" * 60)
    
    # Test 1: Create queue with valid capacity
    print("\n1. Testing queue creation:")
    try:
        q = Queue(5)
        print(f"✅ Queue created with capacity: {q.capacity}")
        q.show()
    except Exception as e:
        print(f"❌ Failed to create queue: {e}")
    
    # Test 2: Create queue with invalid capacity
    print("\n2. Testing invalid capacity:")
    try:
        invalid_q = Queue(0)
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Test 3: Enqueue elements
    print("\n3. Testing enqueue operations:")
    try:
        q = Queue(3)
        q.enqueue(10)
        q.enqueue(20)
        q.enqueue(30)
        print("✅ Successfully enqueued 3 elements")
        q.show()
    except Exception as e:
        print(f"❌ Enqueue failed: {e}")
    
    # Test 4: Enqueue to full queue
    print("\n4. Testing enqueue to full queue:")
    try:
        q.enqueue(40)  # This should fail
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Test 5: Dequeue elements
    print("\n5. Testing dequeue operations:")
    try:
        q = Queue(3)
        q.enqueue(100)
        q.enqueue(200)
        q.enqueue(300)
        
        print("Before dequeue:")
        q.show()
        
        dequeued = q.dequeue()
        print(f"✅ Dequeued element: {dequeued}")
        
        dequeued = q.dequeue()
        print(f"✅ Dequeued element: {dequeued}")
        
        print("After dequeuing twice:")
        q.show()
    except Exception as e:
        print(f"❌ Dequeue failed: {e}")
    
    # Test 6: Dequeue from empty queue
    print("\n6. Testing dequeue from empty queue:")
    try:
        q = Queue(2)
        q.enqueue(1)
        q.dequeue()
        q.dequeue()  # This should fail
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Test 7: Circular queue behavior
    print("\n7. Testing circular queue behavior:")
    try:
        q = Queue(3)
        q.enqueue('A')
        q.enqueue('B')
        q.enqueue('C')
        
        print("Full queue:")
        q.show()
        
        q.dequeue()  # Remove A
        q.enqueue('D')  # Should wrap around
        
        print("After dequeue and enqueue (circular behavior):")
        q.show()
        
        # Test more circular operations
        q.dequeue()  # Remove B
        q.enqueue('E')  # Wrap around again
        
        print("After more circular operations:")
        q.show()
    except Exception as e:
        print(f"❌ Circular queue test failed: {e}")
    
    # Test 8: Mixed operations
    print("\n8. Testing mixed operations:")
    try:
        q = Queue(4)
        q.enqueue(1)
        q.enqueue(2)
        d1 = q.dequeue()
        q.enqueue(3)
        q.enqueue(4)
        d2 = q.dequeue()
        q.enqueue(5)
        
        print(f"✅ Dequeued: {d1}, {d2}")
        print("Final queue after mixed operations:")
        q.show()
    except Exception as e:
        print(f"❌ Mixed operations failed: {e}")
    
    # Test 9: Empty queue state
    print("\n9. Testing empty queue state:")
    try:
        q = Queue(2)
        print(f"✅ Queue is empty: {q.is_empty()}")
        q.enqueue(1)
        print(f"✅ Queue is not empty after enqueue: {not q.is_empty()}")
        q.dequeue()
        print(f"✅ Queue is empty after dequeue: {q.is_empty()}")
    except Exception as e:
        print(f"❌ Empty state test failed: {e}")
    
    # Test 10: Full queue state
    print("\n10. Testing full queue state:")
    try:
        q = Queue(2)
        q.enqueue(1)
        q.enqueue(2)
        print(f"✅ Queue is full: {not q._Queue__is_not_full()}")
        q.dequeue()
        print(f"✅ Queue is not full after dequeue: {q._Queue__is_not_full()}")
    except Exception as e:
        print(f"❌ Full state test failed: {e}")
    
    # Test 11: Boundary case - single element queue
    print("\n11. Testing single element queue:")
    try:
        q = Queue(1)
        q.enqueue("single")
        print("✅ Single-element queue enqueue works")
        q.show()
        dequeued = q.dequeue()
        print(f"✅ Dequeued from single-element queue: {dequeued}")
        q.show()
    except Exception as e:
        print(f"❌ Single element test failed: {e}")
    
    print("\n" + "=" * 60)
    print("Testing completed!")
    print("=" * 60)

def simple_test():
    """简单的功能演示"""
    print("\n" + "=" * 40)
    print("Simple Queue Demo")
    print("=" * 40)
    
    q = Queue(5)
    
    print("Enqueuing elements:")
    for i in range(1, 6):
        q.enqueue(i * 10)
        q.show()
    
    print("\nDequeuing elements:")
    for i in range(3):
        item = q.dequeue()
        print(f"Dequeued: {item}")
        q.show()
    
    print("\nEnqueuing more elements (testing circular behavior):")
    q.enqueue(60)
    q.enqueue(70)
    q.show()

if __name__ == "__main__":
    test_queue()
    simple_test()