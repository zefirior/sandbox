class Tree:
    def __init__(self):
        self._root = None
        self.level = 0

    def __str__(self):
        return str(self._root)

    @property
    def height(self):
        return self._root.height if self._root else 0

    def insert(self, key, value):
        if self._root is None:
            self._root = TreeNode(key, value)
            self._root._parent = self
        else:
            self._root.insert(key, value)

    def replace_child(self, node, new_node):
        if node != self._root:
            raise Exception('Заменяемый узел дерева не совпадает с корнем')
        self._root = new_node
        self._root._parent = self

    def find(self, key):
        return self._root.find(key)


class TreeNode:
    __slots__ = [
        'key',
        'ref',
        '_parent',
        '_left_height',
        '_left',
        '_right_height',
        '_right',
    ]

    def __init__(self, key: int, ref, parent: 'TreeNode' = None):
        self.key = key
        self.ref = ref
        self._parent = parent
        self._left_height = 0
        self._left = None
        self._right_height = 0
        self._right = None

    def __str__(self):
        str_right = self._right or ''
        str_self = '{tab}<{key}>'.format(
            tab='\t' * self.level,
            key=repr(self.key),
            ref=repr(self.ref),
            lh=repr(self._left_height),
            rh=repr(self._right_height),
        )
        str_left = self._left or ''
        return '{}\n{}{}'.format(str_right, str_self, str_left)

    @property
    def level(self):
        if self._parent is None:
            return 0
        else:
            return self._parent.level + 1

    @property
    def height(self):
        return max(self._left_height, self._right_height) + 1

    def mount_left(self, node: 'TreeNode'):
        if node is None:
            self._left = None
        else:
            self._left = node
            self._left._parent = self
        self.calc_height()

    def mount_right(self, node: 'TreeNode'):
        if node is None:
            self._right = None
        else:
            self._right = node
            self._right._parent = self
        self.calc_height()

    def replace_child(self, node, new_node=None):
        if self._left == node:
            # self._left._parent = None
            mount = self.mount_left
        elif self._right == node:
            # self._right._parent = None
            mount = self.mount_right
        else:
            return

        mount(new_node)

    def calc_height(self):
        self._right_height = self._right.height if self._right else 0
        self._left_height = self._left.height if self._left else 0

    def find(self, key):
        if key == self.key:
            return self
        if key < self.key and self._left is not None:
            return self._left.find(key)
        if key > self.key and self._right is not None:
            return self._right.find(key)

    def _right_small_swap(self):
        parent = self._parent
        x_node = self
        y_node = self._right
        beta_subtree = y_node._left

        x_node.mount_right(beta_subtree)
        y_node.mount_left(x_node)

        parent.replace_child(x_node, y_node)

    def _left_small_swap(self):
        parent = self._parent
        x_node = self
        y_node = self._left
        beta_subtree = y_node._right

        x_node.mount_left(beta_subtree)
        y_node.mount_right(x_node)

        parent.replace_child(x_node, y_node)

    def _right_big_swap(self):
        parent = self._parent
        x_node = self
        y_node = self._right
        z_node = y_node._left
        beta_subtree = z_node._left
        gamma_subtree = z_node._right

        x_node.mount_right(beta_subtree)
        y_node.mount_left(gamma_subtree)
        z_node.mount_left(x_node)
        z_node.mount_right(y_node)

        parent.replace_child(x_node, z_node)

    def _left_big_swap(self):
        parent = self._parent
        x_node = self
        y_node = self._left
        z_node = y_node._right
        beta_subtree = z_node._right
        gamma_subtree = z_node._left

        x_node.replace_child(y_node, beta_subtree)
        y_node.replace_child(z_node, gamma_subtree)
        z_node.replace_child(beta_subtree, x_node)
        z_node.replace_child(gamma_subtree, y_node)

        x_node.mount_left(beta_subtree)
        y_node.mount_right(gamma_subtree)
        z_node.mount_right(x_node)
        z_node.mount_left(y_node)

        parent.replace_child(x_node, z_node)

    def _balance(self):
        if -2 < self._left_height - self._right_height < 2:
            return
        elif self._right_height - self._left_height == 2:
            if self._right._right_height - self._right._left_height > -1:
                # print('_right_small_swap')
                self._right_small_swap()
            else:
                # print('_right_big_swap')
                self._right_big_swap()
        elif self._right_height - self._left_height == -2:
            if self._left._left_height - self._left._right_height > -1:
                # print('_left_small_swap')
                self._left_small_swap()
            else:
                # print('_left_big_swap')
                self._left_big_swap()
        else:
            raise Exception

    def insert(self, key, value):
        node = None
        if key == self.key:
            return
        elif key < self.key:
            if self._left is None:
                node = TreeNode(key, value)
                self.mount_left(node)
                self._left_height = self._left.height
            else:
                node = self._left.insert(key, value)
        if key > self.key:
            if self._right is None:
                node = TreeNode(key, value)
                self.mount_right(node)
                self._right_height = self._right.height
            else:
                node = self._right.insert(key, value)
        self.calc_height()
        self._balance()
        return node


def tree_build(dataset):
    if not dataset:
        return
    iterator = enumerate(dataset)
    tree = Tree()

    for i, num in iterator:
        tree.insert(num, i)
        # print('=========')
        # print(tree)
    return tree


if __name__ == '__main__':

    import random
    from time import time as tm

    # dataset_for_find = [1, 6, 23, 546, 234]
    dataset_for_find = [1, 6, 23, 546, 234, 4567, 4356, 8645, 4535]
    dataset = [num for num in range(1, 10000)]
    # random.shuffle(dataset)

    NUM_FIND = 1000

    st = tm()
    tree = tree_build(dataset)

    print(tm() - st)

    st = tm()
    for _ in range(NUM_FIND):
        for key in dataset_for_find:
            node = tree.find(key)
            assert node, 'key={}'.format(key)
            assert node.key == key, 'key={}'.format(key)
    print(tm() - st)

    st = tm()
    for _ in range(NUM_FIND):
        for key in dataset_for_find:
            index = dataset.index(key)
    print(tm() - st)
