
from structpy import specification
from structpy.graph.directed.labeled.multilabeled_digraph_spec import MultiLabeledDigraphSpec


@specification
class MultiLabeledDigraphDataSpec:
    """
    Directed Graph with multiple labels per edge, and attributes
    specified on both nodes and edges.

    Nodes and edge labels can be any hashable object.
    Edge labels are not unique, but nodes are.

    Nodes and edge labels are expected not to be `None`.
    """

    @specification.satisfies(MultiLabeledDigraphSpec.MULTILABELED_DIGRAPH)
    def MULTILABELED_DIGRAPH_DATA(Digraph, edges=None, nodes=None):
        """
        Construct a labeled digraph. Optionally, pass an
        `iterable<tuple<source, target, label>>` of edges and an
        `iterable<node>` of nodes to initialize the graph.

        If the iterables passed for edge and node data are dictonaries,
        values in the dictionary are expected to be attribute dicts defining
        attributes of the corresponding edge/node keys.
        """
        digraph = Digraph({
            ('John', 'Mary', 'likes'): {'a': 1},
            ('Mary', 'Peter', 'likes'): {},
            ('Peter', 'John', 'likes'): {},
            ('Peter', 'Sarah', 'likes'): {}
        }, {
            'Rob': {},
            'John': {'b': 2}
        })
        return digraph

    def data(digraph, node, target=None, label=None):
        """
        Get the attributes associated with a node or edge as an
        `Attributes` object.
        """
        assert digraph.data('John').b == 2
        assert digraph.data('John', 'Mary', 'likes')['a'] == 1



