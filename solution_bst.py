class TreeNode:

    def __init__(self, parent, value):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def insert(self, node):
        """Inserts a node into the subtree rooted at this node.

        Args:
            node: The node to be inserted.
        """
        if node is None:
            return
        if node.value < self.value:
            if self.left is None:
                node.parent = self
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                node.parent = self
                self.right = node
            else:
                self.right.insert(node)


def height(node):
    if not node:
        return 0
    left_height = height(node.left)
    right_height = height(node.right)

    return max(left_height, right_height) + 1


values = []
levels = []


def breadth(root):
    h = height(root)
    for i in range(h):
        print_tree(root, i)
    return values, levels


def print_tree(root, level, acc=0):
    if not root:
        return
    if level == 0:
        values.append(root.value)
        levels.append(acc)
    elif level > 0:
        print_tree(root.left, level - 1, acc + 1)
        print_tree(root.right, level - 1, acc + 1)


def solution():
    arr = list(map(int, input().split()))
    tree = TreeNode(None, arr[0])
    for i in range(1, len(arr)):
        tree.insert(TreeNode(None, arr[i]))
    values, levels = breadth(tree)
    print(' '.join(map(str, values)))
    print(' '.join(map(str, levels)))


solution()