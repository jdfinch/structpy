from structpy.graph import DictionaryGraph

def test_init():
    g = DictionaryGraph()
    assert g._nodes == dict()

def test_add():
    g = DictionaryGraph()
    g.add('a')
    g.add('b', 'c')
    g.add('a', 'b', 1)
    g.add('b', 'c', 2)
    g.add('c', 'a', 3)
    g.add('a', 'd', 4)
    g.add('a', 'e')
    g.add('b', 'f', 5)
    g.add('a')
    
    for char in 'abcde':
        assert char in g._nodes
    
    assert g._nodes['a']['b'] == 1
    assert g._nodes['a']['d'] == 4
    assert g._nodes['a']['e'] == None
    assert g._nodes['b']['c'] == 2
    assert g._nodes['c']['a'] == 3
    assert g._nodes['b']['f'] == 5

    assert 'c' not in g._nodes['a']
    assert None not in g._nodes['a']
    assert None not in g._nodes

    nodes = set('abcdef')
    for node in g.nodes():
        assert node in nodes
        nodes.remove(node)
    assert len(nodes) == 0
    for node in 'abcde':
        assert g.has_node(node)
    assert not g.has_node('g')
    
        



