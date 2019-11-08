
import pytest
from structpy.model.logic_net import LogicNet, logic_node as logic
from structpy import Pointer

def test_constructor():
    lnet = LogicNet()

def test_update():
    lnet = LogicNet()
    cake = Pointer(0.5)
    icecream = Pointer(0.1)
    cake_node = lnet.add(logic.Term(cake))
    icecream_node = lnet.add(logic.Term(icecream))
    cake_or_icecream = lnet.add(logic.Or(icecream_node, cake_node))
    cake_or_icecream.update(1.0)
    assert +cake == 1.0
    assert +icecream == 0.6
