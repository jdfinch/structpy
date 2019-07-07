import pytest
from standard.graph import ListSequence

def test_basic():
    ls = ListSequence([0, 1])
    assert ls.top() == 1
    assert ls.child(0) == 1
    assert ls.child(1) == None
    assert ls.node_at(0) == 0
    assert ls.node_at(1) == 1

def test_traversals():
    ls = ListSequence([0, 1])
    assert list(ls.traverse(0)) == [0,1]
    assert list(ls.traverse(1)) == [1]
    assert list(ls.traverse_reverse(1)) == [1,0]
    assert list(ls.traverse_reverse(0)) == [0]
