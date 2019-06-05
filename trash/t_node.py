from standard.graph import Node

def test_init():
    n = Node(10)
    assert n.get_value() == 10
