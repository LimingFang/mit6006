import random
import sys
import ast
from random import shuffle


class MinBSTNode:
    def __init__(self, parent, val):
        self.left = None
        self.right = None
        self.val = val
        self.parent = parent

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

    def __str__(self):
        return '\n'.join(self._str()[0])

    # 将 val 插入到以 self 为根节点的子树
    def Insert(self, val):
        if val < self.val:
            if self.left is None:
                self.left = MinBSTNode(self, val)
            else:
                self.left.Insert(val)
        else:
            if self.right is None:
                self.right = MinBSTNode(self, val)
            else:
                self.right.Insert(val)

    # 将 val 从以 self 为根节点的子树中删除，返回以 self 为根节点的子树删除后的新子树
    # 前提是 val 得存在
    def Delete(self, val):
        if self.val == val:
            if self.left is None and self.right is None:
                # case1：当前为叶子节点，删除自身
                return None
            elif self.left and self.right:
                # case2: 有2个叶子结点，将 self 替换成右子树中最小的元素，然后从右子树中将其删除
                self.val = self.right.FindMin()
                self.right = self.right.Delete(self.val)
                return self
            else:
                # case3: 只有一个叶子结点
                return self.left if self.left else self.right
        elif val < self.val:
            self.left = self.left.Delete(val)
            return self
        else:
            self.right = self.right.Delete(val)
            return self

    def FindMin(self):
        cur = self
        while (cur.left):
            cur = cur.left
        return cur.val


class MinBST:
    root: MinBSTNode

    def __init__(self):
        self.root = None
        self.len = 0

    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)

    def __len__(self):
        return self.len

    def min(self):
        if not self.root:
            return None
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.val

    def max(self):
        if not self.root:
            return None
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.val

    # return None if not found.
    def find(self, val):
        cur = self.root
        while cur and cur.val != val:
            if cur.val > val:
                cur = cur.left
            else:
                cur = cur.right
        return cur

    def insert(self, val):
        self.len += 1
        if not self.root:
            self.root = MinBSTNode(None, val)
            return

        self.root.Insert(val)
        return

    def delete(self, val):
        ast.Assert(self.root)
        self.len -= 1
        self.root = self.root.Delete(val)

    def next_larger(self, val):
        pass

    def next_smaller(self, val):
        pass


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

    tree = MinBST()
    print(tree)
    for item in items:
        tree.insert(item)
        print()
        print(tree)

    print("=======Delete=======")
    del_items = random.sample(list(items),k=len(tree)//2)
    for item in del_items:
        tree.delete(item)
        print("delete item ", item)
        print(tree)
        print()


if __name__ == '__main__':
    test()
