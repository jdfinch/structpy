
from structpy import specification
from structpy.graph.directed.labeled.multilabeled_parallel_digraph_spec import MultiLabeledParallelDigraphSpec


@specification
class MultiLabeledParallelDigraphDataSpec:
    """
    Directed Graph with multiple labels per edge.
    Unlike MultiLabeledDigraph, multiple edges of the same (s, t, l)
    signature are allowed, because each edge has a unique id.

    Thus edges are identified by their id or a (s, t, l, id) tuple
    instead of by a (s, t, l) tuple.

    Nodes and edge labels can be any hashable object.
    Edge labels are not unique, but nodes are.

    Nodes and edge labels are expected not to be `None`.
    """

    @specification.satisfies(MultiLabeledParallelDigraphSpec.MULTILABELED_PARALLEL_DIGRAPH)
    def MULTILABELED_PARALLEL_DIGRAPH_DATA(Digraph, edges=None, nodes=None):
        """
        Construct a labeled digraph. Optionally, pass an
        `iterable<tuple<source, target, label, id>>` of edges and an
        `iterable<node>` of nodes to initialize the graph.
        """
        digraph = Digraph({
            ('John', 'Mary', 'likes', 'jml'): {'a': 1},
            ('Mary', 'Peter', 'likes', 'mpl'): {},
            ('Peter', 'John', 'likes', 'pjl'): {},
            ('Peter', 'Sarah', 'likes', 'psl'): {}
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
        assert digraph.data('John', 'Mary', 'likes', 'jml')['a'] == 1



