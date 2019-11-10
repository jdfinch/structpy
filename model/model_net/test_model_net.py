
import pytest
from structpy.model.model_net import ModelNet
from structpy.language.primitive import Float
from structpy import I, Pointer

def test_constructor():
    mnet = ModelNet()

def test_update():
    net = ModelNet()
    x = Pointer(0.5)
    y = Pointer(0.1)
    xn = net.add_node(ModelNet.Node(x))
    yn = net.add_node(ModelNet.Node(y))
    zn = ModelNet.Node(
        Pointer(0.0),
        (lambda self: sum(+(t.value()) for t in self.targets())),
        (lambda self, target:
            +target.value() + (
                (+self.value() - sum([+t.value() for t in set(self.targets())]))
                / (len(self.targets())))
        )
    )
    zn.add(xn)
    zn.add(yn)
    net.add_node(zn)
    zn.pull()
    assert +zn.value() == 0.6
    net.push(zn.value(), 0.4)
    assert +x == 0.4
    assert +y == pytest.approx(0.0)
    net.push(y, 0.1)
    assert +zn.value() == 0.4
