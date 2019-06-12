import pytest

from standard.graph import ArraySequence

def test_constructor():
    s = ArraySequence((0,))
    assert s[0] == 0

def test_add():
    s = ArraySequence((0,))
    s.add(1)
    s.add_node(2)
    s.add(3)
    assert s == ArraySequence((0, 1, 2 ,3))

def test_node():
    s = ArraySequence((3, 4, 5, 7))
    assert 4 in s
    assert s.has_node(4)
    assert s.has_arc(4, 5)
    assert not s.has_node(2)
    assert not s.has_arc(5, 4)

def test_traverse():
    l = [3, 4, 5][::-1]
    s = ArraySequence((3, 4, 5))
    for n in s.traverse():
        assert n == l.pop()

def test_traverse_reverse():
    l = [3, 4, 5]
    s = ArraySequence((3, 4, 5))
    for n in s.traverse_reverse():
        assert n == l.pop()

