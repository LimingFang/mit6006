import random
import sys

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

    def IsLeftNode(self):
        return (not self.left) and (not self.right)

class MinBST:
    root: MinBSTNode
    def __init__(self):
        self.root = None

    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)

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
            if cur.val > root:
                cur = cur.left
            else:
                cur = cur.right
        return cur

    def insert(self, val):
        if not self.root:
            self.root = MinBSTNode(None,val)
            return

        cur = self.root
        while (val < cur.val and cur.left) or (val >= cur.val and cur.right):
            cur = cur.left if val < cur.val else cur.right
        if val < cur.val:
            cur.left = MinBSTNode(cur, val)
        else:
            cur.right = MinBSTNode(cur, val)

    def delete(self, val):
        pass

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
        items = (random.randrange(100) for i in range(int(args[0])))
    else:
        items = [int(i) for i in args]

    tree = MinBST()
    print(tree)
    for item in items:
        tree.insert(item)
        print()
        print(tree)

if __name__ == '__main__':
    test()