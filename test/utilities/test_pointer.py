import pytest

from structpy import Pointer

class Simple:

    def __init__(self, a=1, b=2):
        self.one = a
        self.two = b

def test_pointer():
    s = Simple()
    p = Pointer(s)
    s2 = Simple(5, 6)
    p *= s2
    assert p.one == 5
    assert p.two == 6
    assert type(p) is Pointer
    assert p() is s2
    assert +p is s2