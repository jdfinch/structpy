

from structpy import specification
from structpy.graph.directed.labeled.labeled_digraph_spec import LabeledDigraphSpec

@specification
class LabeledDigraphDataSpec:
    """
    Directed Graph with a single label per edge, and attributes
    specified on both nodes and edges.

    Nodes and edge labels can be any hashable object.
    Edge labels are not unique, but nodes are.

    Nodes and edge labels are expected not to be `None`.
    """

    @specification.satisfies(LabeledDigraphSpec.LABELED_DIGRAPH)
    def LABELED_DIGRAPH_DATA(Digraph, edges=None, nodes=None):
        """
        Construct a labeled digraph. Optionally, pass an
        `iterable<tuple<source, target, label>>` of edges and an
        `iterable<node>` of nodes to initialize the graph.

        If the iterables passed for edge and node data are dictonaries,
        values in the dictionary are expected to be attribute dicts defining
        attributes of the corresponding edge/node keys.
        """
        digraph = Digraph([
            ('John', 'Mary', 'likes'),
            ('Mary', 'Peter', 'likes'),
            ('Peter', 'John', 'likes'),
            ('Peter', 'Sarah', 'likes')
        ], ['Rob'])
        return digraph





