from standard.graph import List

def test_constructor():
    l = List((4, 7, 1, 5))

def test_add():
    l = List((3, 4))
    l.add(5)
    assert l == List((3, 4, 5))
    assert l != List((4, 3, 5))
    assert l != List((3, 4, 5, 3))