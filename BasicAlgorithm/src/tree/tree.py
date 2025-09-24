from queue import Queue

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# 这里我们用递归的方式实现创建

def create_binary_tree(input_list: list = []):
    if input_list is None or len(input_list) == 0:
        return None
    data = input_list.pop(0)
    if data is None:
        return None
    node = TreeNode(data=data)
    node.left = create_binary_tree(input_list=input_list)
    node.right = create_binary_tree(input_list=input_list)
    return node


def iter_tree_implementation_one(tree: TreeNode):
    if tree is None:
        return None
    print(tree.data)
    iter_tree_implementation_one(tree=tree.left)
    iter_tree_implementation_one(tree=tree.right)
    return TreeNode


def iter_tree_implementation_two(tree: TreeNode):
    if tree is None:
        return None
    iter_tree_implementation_two(tree=tree.left)
    print(tree.data)
    iter_tree_implementation_two(tree=tree.right)
    return TreeNode


def iter_tree_implementation_three(tree: TreeNode):
    if tree is None:
        return None
    iter_tree_implementation_three(tree=tree.left)
    iter_tree_implementation_three(tree=tree.right)
    print(tree.data)
    return TreeNode


def iter_tree_implementation_four(node: TreeNode):
    stack = []
    result = []
    while (not (node is None)) or stack:
        while not (node is None):
            print(node.data)
            result.append(node)
            stack.append(node)
            node = node.left
        # 先把所有左边的处理到底，并且所有出现过的节点都被存储
        node = stack.pop().right


def iter_tree_bfs(node: TreeNode):
    queue = Queue()
    queue.put(node)
    while not queue.empty():
        node = queue.get()
        print(node.data)
        if node.left is not None:
            queue.put(node.left)
        if node.right is not None:
            queue.put(node.right)
    

if __name__ == '__main__':
    data_list = [1, 2, None, None, 4, 5, 6, 7, 3, None, None, None, 8, None, 9, 10]
    root = create_binary_tree(data_list)

    iter_tree_implementation_one(root)
    print("-"*16)
    iter_tree_implementation_two(root)
    print("-"*16)
    iter_tree_implementation_three(root)
    print("-"*16)
    iter_tree_implementation_four(root)
    print("-"*16)
