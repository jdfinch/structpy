from structpy.graph.frontiers import Queue

def test_constructor():
    l = Queue((4, 7, 1, 5))

def test_add():
    l = Queue((3, 4))
    l.add(5)
    assert l == Queue((3, 4, 5))
    assert l != Queue((4, 3, 5))
    assert l != Queue((3, 4, 5, 3))

def test_iteration():
    l = Queue((3, 4, 5, 6))
    i = 3
    for e in l:
        assert e == i
        i += 1

def test_indexing():
    l = Queue((3, 4, 5, 6))
    assert l[2] == 5
    assert l[0] == 3
    assert l[-1] == 6

def test_pop():
    l = Queue((4, 5, 6))
    assert l.pop() == 4
