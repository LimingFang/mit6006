from bst import MinBST, MinBSTNode
import ast
import sys
import random


def height(node):
    return node.h if node else -1


class MinAVLNode(MinBSTNode):
    def __init__(self, parent, val: int):
        super().__init__(parent, val)
        self.h = 0

    # 左右子树都是 avl tree，但是 h(left_tree) >= h(right_tree)+2
    # 对该节点进行单次右旋（如下图的5），返回新的根节点（3），所有子节点高度都更新
    #       6
    #      / \
    #     5  9
    #    /
    #   3
    #  /
    # 1
    def SingleRightRotate(self):
        ast.Assert(self.h >= 2)

        res = self.left
        self.left = res.right
        res.right = self
        if self.parent is not None:
            if self.parent.left is self:
                self.parent.left = res
            else:
                self.parent.right = res
        res.parent = self.parent
        self.parent = res

        self.h = max(height(self.right), height(self.left)) + 1
        res.h = max(height(res.right), height(res.left)) + 1

        return res

    def SingleLeftRotate(self):
        ast.Assert(self.h >= 2)

        res = self.right
        self.right = res.left
        res.left = self

        if self.parent is not None:
            if self.parent.left is self:
                self.parent.left = res
            else:
                self.parent.right = res
        res.parent = self.parent
        self.parent = res

        self.h = max(height(self.right), height(self.left)) + 1
        res.h = max(height(res.right), height(res.left)) + 1

        return res

    # 插入前以 self 为根节点的树是 avl tree，插入后后不一定，由 AVL 进行 rebalance
    # 返回插入的那个节点
    def Insert(self, val):
        res = None
        if val < self.val:
            if self.left is None:
                self.left = MinAVLNode(self, val)
                res = self.left
            else:
                res = self.left.Insert(val)
        else:
            if self.right is None:
                self.right = MinAVLNode(self, val)
                res = self.right
            else:
                res = self.right.Insert(val)

        return res

    # 将 self 从以自己为根节点的 AVL Tree 中删除，返回真正删除的节点。
    def Delete(self):
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.right or self.left
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.right or self.left
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            delete_node = self.FindMin()
            ast.Assert(delete_node and (delete_node is not self))
            self.val, delete_node.val = delete_node.val, self.val
            return delete_node.Delete()

    def FindMin(self):
        cur = self
        while cur.left.h >= 0:
            cur = cur.left
        return cur

    def _str(self):
        """Internal method for ASCII art."""
        label = str(self.val)
        if self.left is None:
            left_lines, left_pos, left_width = [], 0, 0
        else:
            left_lines, left_pos, left_width = self.left._str()
        if self.right is None:
            right_lines, right_pos, right_width = [], 0, 0
        else:
            right_lines, right_pos, right_width = self.right._str()
        middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
        pos = left_pos + middle // 2
        width = left_pos + middle + right_width - right_pos
        while len(left_lines) < len(right_lines):
            left_lines.append(' ' * left_width)
        while len(right_lines) < len(left_lines):
            right_lines.append(' ' * right_width)
        if (middle - len(label)) % 2 == 1 and self.parent is not None and \
                self is self.parent.left and len(label) < middle:
            label += '.'
        label = label.center(middle, '.')
        if label[0] == '.': label = ' ' + label[1:]
        if label[-1] == '.': label = label[:-1] + ' '
        lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle - 2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
                [left_line + ' ' * (width - left_width - right_width) + right_line
                 for left_line, right_line in zip(left_lines, right_lines)]
        return lines, pos, width


class MinAVL(MinBST):
    root: MinAVLNode

    def __init__(self):
        super().__init__()
        # dummy node
        self.root = None
        self.len = 0

    def __len__(self):
        return self.len

    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)

    # 将 val 插入的同时，维持 AVL 属性
    def insert(self, val):
        self.len += 1
        if not self.root:
            self.root = MinAVLNode(None, val)
        else:
            node = self.root.Insert(val)
            self.rebalance(node.parent)

    # 将 val 从 AVL Tree 中删除，保持 avl 属性
    def delete(self, val):
        self.len -= 1
        delete_node = self.find(val)
        if delete_node is self.root:
            pseudo_root = MinAVL()
            pseudo_root.root = MinAVLNode(None, val + 1)
            pseudo_root.root.left = self.root
            self.root.parent = pseudo_root.root
            delete_node = self.root.Delete()
            self.root = pseudo_root.root.left
            if self.root:
                self.root.parent = None
            if delete_node.parent is not pseudo_root.root:
                self.rebalance(delete_node.parent)
        else:
            delete_node = delete_node.Delete()
            self.rebalance(delete_node.parent)

    # 从 node 开始做 AVL Rebalance 直到 root
    # 保证 node 左右子树是 AVL Tree
    def rebalance(self, node: MinAVLNode):
        last_node = None
        while node is not None:
            if height(node.left) - height(node.right) >= 2:
                # much too left-heavy => node=k+2, left=k+1, right=k-1
                if height(node.left.left) >= height(node.left.right):
                    node = node.SingleRightRotate()
                else:
                    node.left.SingleLeftRotate()
                    node = node.SingleRightRotate()
            elif height(node.right) - height(node.left) >= 2:
                if height(node.right.right) >= height(node.right.left):
                    node = node.SingleLeftRotate()
                else:
                    node.right.SingleRightRotate()
                    node = node.SingleLeftRotate()

            last_node = node
            node = node.parent
        self.root = last_node


def test(args=None):
    if not args:
        args = sys.argv[1:]
    if not args:
        print('usage: %s <number-of-random-items | item item item ...>' % \
              sys.argv[0])
        sys.exit()
    elif len(args) == 1:
        items = [random.randrange(100) for i in range(int(args[0]))]
    else:
        items = [int(i) for i in args]
    print(items)
    tree = MinAVL()
    print(tree)
    for item in items:
        tree.insert(item)
    print(tree)

    print("=======Delete=======")
    del_items = random.sample(list(items), k=len(tree) // 2)
    for item in del_items:
        print("delete item ", item)
        tree.delete(item)
        print(tree)
        print()


if __name__ == "__main__":
    test()
