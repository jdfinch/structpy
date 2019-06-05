from standard.graph import List

def test_constructor():
    l = List((4, 7, 1, 5))

def test_add():
    l = List((3, 4))
    l.add(5)
    assert l == List((3, 4, 5))
    assert l != List((4, 3, 5))
    assert l != List((3, 4, 5, 3))

def test_iteration():
    l = List((3, 4, 5, 6))
    i = 3
    for e in l:
        assert e == i
        i += 1
    
def test_indexing():
    l = List((3, 4, 5, 6))
    assert l[2] == 5
    assert l[0] == 3
    assert l[-1] == 6