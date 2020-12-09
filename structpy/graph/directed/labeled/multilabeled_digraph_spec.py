
from structpy import specification


@specification
class MultiLabeledDigraphSpec:
    """
    Directed Graph with multiple labels per edge.

    Nodes and edge labels can be any hashable object.
    Edge labels are not unique, but nodes are.

    Nodes and edge labels are expected not to be `None`.
    """

    @specification.init
    def MULTILABELED_DIGRAPH(Digraph, edges=None, nodes=None):
        """
        Construct a labeled digraph. Optionally, pass an
        `iterable<tuple<source, target, label>>` of edges and an
        `iterable<node>` of nodes to initialize the graph.
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

        Three parameters tests for `target-target-label` edge membership.
        """
        assert digraph.has('John')
        assert digraph.has('Rob')

        assert digraph.has('John', 'Mary', 'likes')
        assert digraph.has('Peter', 'Sarah', 'likes')

        assert digraph.has('John', label='likes')
        assert digraph.has('John', 'Mary')

        assert not digraph.has('Sarah', 'Peter', 'likes')
        assert not digraph.has('George')

    def targets(digraph, source, label=None):
        """
        Get all of the _targets along out-edges of a given target.

        Providing a label filters the results based on edge label.
        """
        assert digraph.targets('Peter') == {'John', 'Sarah'}

    def sources(digraph, target, label=None):
        """
        Get all of the sources along in-edges of a given target.

        Providing a label filters the results based on edge label.
        """
        assert digraph.sources('Mary') == {'John'}

    def neighbors(digraph, node, label=None):
        """
        Get all of the neighboring nodes of a given node.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.neighbors('Mary')) == {'John', 'Peter'}

    def out_edges(digraph, source, label=None):
        """
        Return an iterable over all out-edges of `target`.

        Providing a label filters the results based on edge label.
        """
        oe = digraph.out_edges('Peter')
        cmp = {('Peter', 'John', 'likes'), ('Peter', 'Sarah', 'likes')}
        assert oe == cmp

    def in_edges(digraph, target, label=None):
        """
        Return an iterable over all in-edges of `target`.

        Providing a label filters the results based on edge label.
        """
        assert digraph.in_edges('Mary') == {('John', 'Mary', 'likes')}

    def nodes(digraph):
        """
        Return an iterable over all nodes in the digraph.
        """
        assert digraph.nodes() == {'Mary', 'John', 'Rob', 'Peter', 'Sarah'}

    def edges(digraph, node=None, label=None):
        """
        Return an iterable over all edges in the digraph, each edge represented by a
        `tuple<target, target, edge_label>`.

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

        digraph.add('Mary', 'George', 'None')
        assert digraph.has('Mary', 'George', 'None')

        # More than one label is allowed per edge
        digraph.add('John', 'Mary', 'dislikes')
        assert digraph.has('John', 'Mary', 'likes')
        assert digraph.has('John', 'Mary', 'dislikes')

    def remove(digraph, node, target=None, label=None):
        """
        Remove a node or edge.

        Edge removal can be specified by specifying the `target` and 'label'
        of the out-edge of `node`.

        Removing a node removes all connected in- and out-edges.
        """
        digraph.remove('Rick')
        assert not digraph.has('Rick')
        assert not digraph.has('George', 'Rick', 'dislikes')
        assert digraph.has('George')

        digraph.remove('Mary', 'George', 'None')
        assert not digraph.has('Mary', 'George', 'None')

        digraph.remove('John', 'Mary', 'likes')
        assert not digraph.has('John', 'Mary', 'likes')
        assert digraph.has('John', 'Mary', 'dislikes')

    def set(digraph, node, target, old_label=None, new_label=None):
        """
        Replaces a node or an edge label.

        Two arguments replaces `node` with `target`, where all edges are preserved.

        Four arguments replaces the edge 'old_label' from `node` to `target` with `new_label`.
        """
        digraph.set('Peter', 'Pete')
        assert not digraph.has('Peter')
        assert digraph.has('Pete')
        assert digraph.has('Pete', 'Sarah', 'likes')

        digraph.set('Pete', 'Sarah', 'likes', 'dislikes')
        assert not digraph.has('Pete', 'Sarah', 'likes')
        assert digraph.has('Pete', 'Sarah', 'dislikes')

