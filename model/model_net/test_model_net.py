
import pytest
from structpy.model.model_net import ModelNet
from structpy import Pointer, I

def test_constructor():
    lnet = ModelNet()

def test_update():
    net = ModelNet()
    x = Pointer(0.5)
    y = Pointer(0.1)
    xn = net.add_node(ModelNet.Node(x))
    yn = net.add(y)
    zn = I(
        ModelNet.Node(None, xn, yn),
        pull_val=(lambda self: sum(+(t.value) for t in self.targets())),
        push_val=(
            lambda self, target:
                self.value
                - sum([+t for t in set(self.targets()) - {target}]) / 2
        )
    )
    zn = net.add_node(ModelNet.Node(Pointer(0.0)))
    zn.pull()
    assert +zn.value == 0.6
    net.push_node(zn, 0.4)
    assert +x == 0.4
    assert +y == 0.0
    net.push(y, 0.1)
    assert +zn.value == 0.5
