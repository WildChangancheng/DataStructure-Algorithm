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


def calculate_indice(indice:int, type):
    if type == 'left':
        return 2 * indice + 1
    if type == 'right':
        return 2 * indice + 2
    

def exchange_elements(lst: list, indice1: int, indice2: int):
    return


def self_adjust(tree: Node):
    lst_tree = storage_binary_in_list([i.val for i in tree])
    layer = num_of_layer(tree)

    for i in range(1, layer)[::-1]:
        # 从倒数第二行开始，所以不用管最后一层
        for j in range(2 ** (i-1), 2 ** i, 1):
            # 2^i即第i+1行的第一个元素的序号，作为index记得-1
            ele = lst_tree[j-1]
            ele_left = lst_tree[calculate_indice(j, 'left')]
            ele_right = lst_tree[calculate_indice(j, 'right')]
            if (ele > ele_left) and (ele > ele_right):
                continue
            


    return 


if __name__ == "__main__":
    tree = create_tree_from_list([1, 2, 3, None, None, 4, None, None, 5, 6, None, None, 7, None , None])
    print(tree)
    lst_tree = [i.val for i in storage_binary_in_list(tree)]
    print(num_of_layer(tree=tree))

    print(lst_tree)

