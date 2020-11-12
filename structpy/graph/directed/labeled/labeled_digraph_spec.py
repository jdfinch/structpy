
from structpy import specification


@specification
class LabeledDigraphSpec:
    """
    Directed Graph with a single label per edge.

    Nodes and edge labels can be any hashable object.
    Edge labels are not unique, but nodes are.

    Nodes and edge labels are expected not to be `None`.
    """

    @specification.init
    def LABELED_DIGRAPH(Digraph, edges=None, nodes=None):
        """
        Construct a labeled digraph. Optionally, pass an
        `iterable<tuple<source, target, label>>` of edges and an
        `iterabele<node>` of nodes to initialize the graph.
        """
        digraph = Digraph([
            ('John', 'Mary', 'likes'),
            ('Mary', 'Peter', 'likes'),
            ('Peter', 'John', 'likes'),
            ('Peter', 'Sarah', 'likes')
        ], ['Rob'])
        return digraph

    def has(digraph, node, target=None, label=None):
        """
        Test membership of a node or edge.

        One parameter tests node membership.

        Specifying `node` and `target` tests whether there is an edge between nodes.

        Specifying `node` and `label` tests whether `node` has an out-edge with `label`.

        Three parameters tests for `source-target-label` edge membership.
        """
        assert digraph.has('John')
        assert digraph.has('Rob')

        assert digraph.has('John', 'Mary', 'likes')
        assert digraph.has('Peter', 'Sarah', 'likes')

        assert digraph.has('John', label='likes')
        assert digraph.has('John', 'Mary')

        assert not digraph.has('Sarah', 'Peter', 'likes')
        assert not digraph.has('George')

    def target(digraph, source, label):
        """
        Get a target given a source and label.
        """
        assert digraph.target('Mary', 'likes') == 'Peter'

    def source(digraph, target, label):
        """
        Get the source of an edge given a target and label.
        """
        assert digraph.source('Peter', 'likes') == 'Mary'

    def targets(digraph, source, label=None):
        """
        Get all of the targets along out-edges of a given source.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.targets('Peter')) == {'John', 'Sarah'}

    def sources(digraph, target, label=None):
        """
        Get all of the sources along in-edges of a given target.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.sources('Mary')) == {'John'}

    def neighbors(digraph, node, label=None):
        """
        Get all of the neighboring nodes of a given node.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.neighbors('Mary')) == {'John', 'Peter'}

    def out_edges(digraph, source, label=None):
        """
        Return an iterable over all out-edges of `source`.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.out_edges('Peter')) == {
            ('Peter', 'John', 'likes'),
            ('Peter', 'Sarah', 'likes')
        }

    def in_edges(digraph, target, label=None):
        """
        Return an iterable over all in-edges of `target`.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.in_edges('Mary')) == {('John', 'Mary', 'likes')}

    def nodes(digraph):
        """
        Return an iterable over all nodes in the digraph.
        """
        assert set(digraph.nodes()) == {'Mary', 'John', 'Rob', 'Peter', 'Sarah'}

    def edges(digraph, node=None, label=None):
        """
        Return an iterable over all edges in the digraph, each edge represented by a
        `tuple<source, target, edge_label>`.

        If a `node` is provide, only provides edges neighboring that node.

        Providing a label filters results by edge label.
        """
        assert set(digraph.edges()) == {
                ('John', 'Mary', 'likes'),
                ('Mary', 'Peter', 'likes'),
                ('Peter', 'John', 'likes'),
                ('Peter', 'Sarah', 'likes')
        }

        assert set(digraph.edges('Mary')) == {
            ('John', 'Mary', 'likes'),
            ('Mary', 'Peter', 'likes')
        }

        assert set(digraph.edges(label='likes')) == {
            ('John', 'Mary', 'likes'),
            ('Mary', 'Peter', 'likes'),
            ('Peter', 'John', 'likes'),
            ('Peter', 'Sarah', 'likes')
        }

    def add(digraph, node, target=None, label=None):
        """
        Add a node or edge.

        One parameter adds a node.

        Three parameters adds an edge.
        """
        digraph.add('George')
        assert digraph.has('George')

        digraph.add('George', 'Rick', 'dislikes')
        assert digraph.has('George', 'Rick', 'dislikes')

        digraph.add('Mary', 'George')
        assert digraph.has('Mary', 'George', None)

        # Only one label is allowed per edge
        digraph.add('John', 'Mary', 'dislikes')
        assert not digraph.has('John', 'Mary', 'likes')
        assert digraph.has('John', 'Mary', 'dislikes')

    def remove(digraph, node, target=None, label=None):
        """
        Remove a node or edge.

        Edge removal can be specified by specifying the `label` or `target`
        of the source `node`.

        Removing a node removes all connected in- and out-edges.
        """
        digraph.remove('Rick')
        assert not digraph.has('Rick')
        assert not digraph.has('George', 'Rick', 'dislikes')
        assert digraph.has('George')

        digraph.remove('Mary', 'George')
        assert not digraph.has('Mary', 'George')

        digraph.remove('John', label='dislikes')
        assert not digraph.has('John', 'Mary')

    def set(digraph, node, target, new_label=None):
        """
        Replaces a node or an edge label.

        Two arguments replaces `node` with `target`, where all edges are preserved.

        Three arguments replaces the edge from `node` to `target` with `new_label`.
        """
        digraph.set('Peter', 'Pete')
        assert not digraph.has('Peter')
        assert digraph.has('Pete')
        assert digraph.has('Sarah', 'Pete', 'likes')

        digraph.set('Sarah', 'Pete', 'dislikes')
        assert not digraph.has('Sarah', 'Pete', 'likes')
        assert digraph.has('Sarah', 'Pete', 'dislikes')

