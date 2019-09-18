
from structpy.utilities import PointerFunnel, PointerFunnelItem

class Foo:

    def __init__(self):
        self.a = 5
        self.b = 3

    def bat(self, x):
        return self.a + x


class Bar:

    def baz(self, x, y):
        return x ** 2 + y

def test_pointer_funnel():
    f = Foo()
    b = Bar()
    pf1 = PointerFunnel(f)
    assert pf1.pf_item is f
    pf2 = PointerFunnel(pf1)
    assert pf2.pf_item is f
    pf1.pf_point(b)
    assert pf1.pf_item is b
    assert pf2.pf_item is b
    pf3 = PointerFunnel(pf2)
    assert pf3.pf_item is b
    pf1.pf_point(f)
    assert pf1.pf_item is f
    assert pf2.pf_item is f
    assert pf3.pf_item is f
    pf2.pf_point(b)
    assert pf1.pf_item is f
    assert pf2.pf_item is b
    assert pf3.pf_item is b
    assert pf2.pf_target is None
    assert pf1.pf_sources == set()

def test_pointer_funnel_item():
    f = Foo()
    b = Bar()
    pf1 = PointerFunnelItem(f)
    assert pf1.pf_item is f
    pf2 = PointerFunnelItem(pf1)
    assert pf2.pf_item is f
    pf1.pf_point(b)
    assert pf1.pf_item is b
    assert pf2.pf_item is b
    pf3 = PointerFunnelItem(pf2)
    assert pf3.pf_item is b
    pf1.pf_point(f)
    assert pf1.pf_item is f
    assert pf2.pf_item is f
    assert pf3.pf_item is f
    pf2.pf_point(b)
    assert pf1.pf_item is f
    assert pf2.pf_item is b
    assert pf3.pf_item is b
    assert pf2.pf_target is None
    assert pf1.pf_sources == set()
    assert pf1.a == 5
    assert pf1.bat(3) == 8
    assert pf2.baz(1, 2) == 3

def test_pointer_funnel_leveling():
    f = Foo()
    b = Bar()
    pf1 = PointerFunnelItem(f)
    pf2 = PointerFunnelItem(pf1)
    pf3 = PointerFunnelItem(pf2)
    pf1.pf_point(b)
    pf4 = PointerFunnel(pf3, 0)
    assert pf4.pf_target is None
    assert pf4.pf_item is b
    pf4.pf_point(pf2, 1)
    assert pf4.pf_target is pf1
    assert pf4.pf_item is b
    pf4 = PointerFunnel(pf3, 3)
    assert pf4.pf_target is pf3
    assert pf4.pf_item is b
