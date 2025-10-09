from binarytree import Node
from queue import Queue

def create_tree_from_list(input_list: list):
    if (not input_list) or (input_list is None):
        return None
    data = input_list.pop(0)
    if data is None:
        return None
    node = Node(data)
    node.left = create_tree_from_list(input_list=input_list)
    node.right = create_tree_from_list(input_list=input_list)
    return node


def storage_binary_in_list(node: Node) -> list[Node]:
    result = []
    # 这个实现只有满二叉树形状才可以用
    
    queue = Queue()
    queue.put(node)
    while not queue.empty():
        node = queue.get()
        result.append(node)
        if node.left is not None:
            queue.put(node.left)
        if node.right is not None:
            queue.put(node.right)

    return result


def num_of_layer(tree: Node):
    num = 1
    node = tree
    while not (node.left is None):
        num += 1
        node = node.left
    return num


def adjust_tree(tree: Node):
    # 把树转成数组存储（假设下标从0开始）
    lst_tree = [i.val for i in storage_binary_in_list(tree)]
    n = len(lst_tree)

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    def heap_to_tree(heap, i=0):
        if i >= len(heap):
            return None
        
        root = Node(heap[i])
        root.left = heap_to_tree(heap, 2 * i + 1)
        root.right = heap_to_tree(heap, 2 * i + 2)
        return root

    # 从最后一个非叶子结点开始往上堆化
    for i in range(n // 2 - 1, -1, -1):
        heapify(lst_tree, n, i)
    return heap_to_tree(lst_tree)

if __name__ == "__main__":
    tree = create_tree_from_list([1, 2, 3, None, None, 4, None, None, 5, 6, None, None, 7, None , None])
    print(tree)
    lst_tree = [i.val for i in storage_binary_in_list(tree)]
    print(num_of_layer(tree=tree))

    print(lst_tree)
    print(adjust_tree(tree))

