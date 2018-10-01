from binary_tree import TreeNode, tree_build

VALUE = 'some_value'
SOME_KEY = 30


def build_abstract_tree(level, node: TreeNode = None):
    node = node or TreeNode(SOME_KEY, VALUE)
    if level > 1:
        left = TreeNode(SOME_KEY, VALUE)
        build_abstract_tree(level - 1, left)
        node.mount_left(left)

        right = TreeNode(SOME_KEY, VALUE)
        build_abstract_tree(level - 1, right)
        node.mount_right(right)

    return node


def test_build_abstract_tree():
    root = build_abstract_tree(1)

    assert isinstance(root, TreeNode)
    assert root._left is None
    assert root._right is None

    root = build_abstract_tree(2)

    assert isinstance(root, TreeNode)
    assert isinstance(root._left, TreeNode)
    assert isinstance(root._right, TreeNode)


def test_basic_behavior():
    node1 = TreeNode(5, VALUE)
    node2 = TreeNode(5, VALUE)

    assert node1 == node1
    assert node1 != node2


def test_mount():
    root = TreeNode(5, VALUE)
    sub_node = TreeNode(3, VALUE)
    root.mount_left(sub_node)

    assert sub_node == root._left
    assert sub_node._parent == root
    assert root._right_height == 0
    assert root._left_height == 1


def test_replace_child():
    root = TreeNode(5, VALUE)
    sub_node = TreeNode(3, VALUE)
    root.mount_left(sub_node)

    assert sub_node == root._left
    assert sub_node._parent == root

    new_sub_node = TreeNode(3, VALUE)
    root.replace_child(sub_node, new_sub_node)

    assert root._left != sub_node
    assert root._left == new_sub_node

    root.replace_child(new_sub_node, None)

    assert root._left is None


def test_tree_build():
    key_list = [10, 5, 15]
    tree = tree_build(key_list)
    root = tree._root

    assert root.key == 10
    assert root._left.key == 5
    assert root._right.key == 15


def test_small_swap():
    alfa_tree = build_abstract_tree(level=3)
    beta_tree = build_abstract_tree(level=4)
    gamma_tree = build_abstract_tree(level=4)

    x_node = TreeNode(SOME_KEY, VALUE)
    y_node = TreeNode(SOME_KEY, VALUE)

    y_node.mount_left(beta_tree)
    y_node.mount_right(gamma_tree)

    x_node.mount_left(alfa_tree)
    x_node.mount_right(y_node)

    x_node._right_small_swap()

    assert x_node._left == alfa_tree
    assert x_node._right == beta_tree
    assert y_node._left == x_node
    assert y_node._right == gamma_tree
    assert y_node._parent is None


def test_big_swap():
    alfa_tree = build_abstract_tree(level=3)
    beta_tree = build_abstract_tree(level=3)
    gamma_tree = build_abstract_tree(level=3)
    psi_tree = build_abstract_tree(level=3)

    x_node = TreeNode(SOME_KEY, VALUE)
    y_node = TreeNode(SOME_KEY, VALUE)
    z_node = TreeNode(SOME_KEY, VALUE)

    z_node.mount_left(beta_tree)
    z_node.mount_right(gamma_tree)

    y_node.mount_left(z_node)
    y_node.mount_right(psi_tree)

    x_node.mount_left(alfa_tree)
    x_node.mount_right(y_node)

    x_node._right_big_swap()

    assert x_node._left == alfa_tree
    assert x_node._right == beta_tree
    assert y_node._left == gamma_tree
    assert y_node._right == psi_tree
    assert z_node._left == x_node
    assert z_node._right == y_node
    assert z_node._parent is None
