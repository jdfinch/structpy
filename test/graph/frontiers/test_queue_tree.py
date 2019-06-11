import pytest

from standard.graph.frontiers import QueueTree, Queue

def test_constructor():
    qt = QueueTree('a')
    qt2 = QueueTree('a', (1, 2, 3))
    assert qt.root() == 'a'
    assert len(qt2._nodes) == 4
    assert len(qt2) == 4
    assert qt2._active == 'a'

def test_add():
    qt = QueueTree('a')
    qt.add('b')
    qt.add('c')
    assert qt.pop() == 'a'
    assert qt.pop() == 'b'
    qt.add('d')
    assert qt.has_arc('a', 'b')
    assert qt.has_arc('a', 'c')
    assert qt.has_arc('b', 'd')
    assert qt.pop() == 'c'