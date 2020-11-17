from structpy.graph.directed.labeled.labeled_digraph_networkx import LabeledDigraphNX
from structpy.map.bijective.bimap import Bimap

class ConceptGraph:

    def __init__(self, edges=None, nodes=None):
        self.next_id = 0
        self.graph = LabeledDigraphNX(edges, nodes)
        if edges is not None:
            self.predicate_map = Bimap(
                {edge: '-'.join(edge) for edge in edges}
            )
        else:
            self.predicate_map = Bimap()

    def get_next_id(self):
        to_return = self.next_id
        self.next_id += 1
        return to_return

    def add_node(self, node):
        """
        Add a node.
        """
        self.graph.add(node)

    def add_predicate(self, source, target, label, predicate_id=None):
        """
        Add a predicate with optional predicate_id.
        Otherwise, predicate_id is automatically generated.
        :return: predicate_id
        """
        if predicate_id is None:
            predicate_id = '%s-%s-%s' % (source, target, label)
        self.graph.add(source, target, label)
        self.predicate_map[(source, target, label)] = predicate_id
        return predicate_id

    def remove(self, node, target=None):
        """
        Remove a node or edge.

        Edge removal can be specified by specifying the `target`
        of the out-edge of `node`.

        Removing a node removes all connected in- and out-edges.
        """
        edges = list(self.predicate_map.items())
        if target is None:
            for edge, edge_id in edges:
                if edge[0] == node or edge[1] == node:
                    del self.predicate_map[edge]
            self.graph.remove(node)
        else:
            for edge, edge_id in edges:
                if edge[0] == node and edge[1] == target:
                    del self.predicate_map[edge]
            self.graph.remove(node, target)

    def nodes(self):
        pass

if __name__ == '__main__':
    cg = ConceptGraph([
        ('John', 'Mary', 'likes'),
        ('Mary', 'Peter', 'likes'),
        ('Peter', 'John', 'likes'),
        ('Peter', 'Sarah', 'likes')
        ], ['Rob'])

    assert cg.predicate_map[('John', 'Mary', 'likes')] == 'John-Mary-likes'
    assert cg.predicate_map.reverse()['John-Mary-likes'] == ('John', 'Mary', 'likes')

    pred_id = cg.add_predicate('Peter', 'Mary', 'hates', 'new_id')

    assert pred_id == 'new_id'
    assert cg.graph.has('Peter', 'Mary', 'hates')
    assert cg.predicate_map[('Peter', 'Mary', 'hates')] == 'new_id'
    assert cg.predicate_map.reverse()['new_id'] == ('Peter', 'Mary', 'hates')

    cg.remove('Mary')
    assert not cg.graph.has('Mary')
    assert cg.graph.has('John')
    assert cg.graph.has('Peter')
    assert not cg.graph.has('John', 'Mary', 'likes')
    assert not cg.graph.has('Mary', 'Peter', 'likes')
    assert not cg.graph.has('Peter', 'Mary', 'hates')
    assert ('John', 'Mary', 'likes') not in cg.predicate_map
    assert ('Mary', 'Peter', 'likes') not in cg.predicate_map
    assert ('Peter', 'Mary', 'hates') not in cg.predicate_map

    cg.remove('Peter', 'John')
    assert cg.graph.has('Peter')
    assert cg.graph.has('John')
    assert not cg.graph.has('Peter', 'John', 'likes')
    assert ('Peter', 'John', 'likes') not in cg.predicate_map

    test = 1

    cg = ConceptGraph()
    in0 = cg.add_predicate('i', 'movie', 'likes')
    in1 = cg.add_predicate('acting', 'good', 'was')
    in2 = cg.add_predicate(in0, in1, 'because', 'nested_pred')
    in3 = cg.add_predicate('you', 'nested_pred', 'hate')

    assert