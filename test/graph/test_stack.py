from standard.graph import Stack

def test_constructor():
    l = Stack((4, 7, 1, 5))

def test_add():
    l = Stack((3, 4))
    l.add(5)
    assert l == Stack((3, 4, 5))
    assert l != Stack((4, 3, 5))
    assert l != Stack((3, 4, 5, 3))

def test_iteration():
    l = Stack((3, 4, 5, 6))
    i = 3
    for e in l:
        assert e == i
        i += 1
    
def test_indexing():
    l = Stack((3, 4, 5, 6))
    assert l[2] == 5
    assert l[0] == 3
    assert l[-1] == 6

def test_pop():
    l = Stack((4, 5, 6))
    assert l.pop() == 6
    