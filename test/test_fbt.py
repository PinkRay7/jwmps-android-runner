from zrTest.functions import all_possible_fbt, all_possible_fbt_memo

def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)

def test_fbt_one_node():
    # N = 1, return tree with 1 node
    trees = all_possible_fbt(1)
    assert len(trees) == 1
    assert count_nodes(trees[0]) == 1

def test_fbt_two_node():
    # N = 3, return tree with 2 nodes
    trees = all_possible_fbt(3)
    assert len(trees) == 1
    assert count_nodes(trees[0]) == 3

def test_fbt_multi_nodes():
    # N = 5, return trees with multiple nodes
    trees = all_possible_fbt(5)
    assert len(trees) == 2  # might have 2 structures
    for tree in trees:
        assert count_nodes(tree) == 5

def test_fbt_multi_struc():
    # N = 7, return trees with multiple structures
    trees = all_possible_fbt(7)
    assert len(trees) == 5  # should have 5 structures
    for tree in trees:
        assert count_nodes(tree) == 7

def test_fbt_empty():
    trees = all_possible_fbt(2)
    assert trees == []

# --- TEST MEMO VERSION ---
def test_fbt_one_node_m():
    # N = 1, return tree with 1 node
    trees = all_possible_fbt_memo(1)
    assert len(trees) == 1
    assert count_nodes(trees[0]) == 1

def test_fbt_two_node_m():
    # N = 3, return tree with 2 nodes
    trees = all_possible_fbt_memo(3)
    assert len(trees) == 1
    assert count_nodes(trees[0]) == 3

def test_fbt_multi_nodes_m():
    # N = 5, return trees with multiple nodes
    trees = all_possible_fbt_memo(5)
    assert len(trees) == 2  # might have 2 structures
    for tree in trees:
        assert count_nodes(tree) == 5

def test_fbt_multi_struc_m():
    # N = 7, return trees with multiple structures
    trees = all_possible_fbt_memo(7)
    assert len(trees) == 5  # should have 5 structures
    for tree in trees:
        assert count_nodes(tree) == 7

def test_fbt_empty():
    trees = all_possible_fbt_memo(2)
    assert trees == []