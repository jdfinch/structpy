import pytest

from structpy import Pointer, PointerItem

class Simple:

    def __init__(self, a=1, b=2):
        self.one = a
        self.two = b

def test_pointer():
    s = Simple()
    p = PointerItem(s)
    s2 = Simple(5, 6)
    p *= s2
    assert p.one == 5
    assert p.two == 6
    assert +p is s2
    assert isinstance(p, Pointer)
    assert isinstance(p, Simple)