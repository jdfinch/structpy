from structpy.collections import Queue
from collections import deque

def test_constructor():
    q = Queue()
    assert q == deque()
    q = Queue((1, 2, 3))
    assert q == deque((1, 2, 3))

def test_add():
    q = Queue()
    q.add(1)
    q.add(2)
    assert q == deque((1, 2))

def test_pop():
    q = Queue((1, 2, 3))
    assert q.pop() == 1
    assert q.pop() == 2
    assert q.pop() == 3
    assert len(q) == 0

def test_top():
    q = Queue((1, 2, 3))
    assert q.top() == 1

def test_obj():
    q = Queue()
    d = {}
    d[q] = 0
    assert d[q] == 0