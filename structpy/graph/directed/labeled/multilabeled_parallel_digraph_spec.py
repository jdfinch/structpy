
from structpy import specification


@specification
class MultiLabeledParallelDigraphSpec:
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

    @specification.init
    def MULTILABELED_PARALLEL_DIGRAPH(Digraph, edges=None, nodes=None):
        """
        Construct a labeled digraph. Optionally, pass an
        `iterable<tuple<source, target, label, id>>` of edges and an
        `iterable<node>` of nodes to initialize the graph.
        """
        digraph = Digraph([
            ('John', 'Mary', 'likes', 'jml'),
            ('Mary', 'Peter', 'likes', 'mpl'),
            ('Peter', 'John', 'likes', 'pjl'),
            ('Peter', 'Sarah', 'likes', 'psl')
        ], ['Rob'])
        return digraph

    def has(digraph, node=None, target=None, label=None, edge_id=None):
        """
        Test membership of a node or edge.

        One parameter tests node membership.

        Specifying `node` and `target` tests whether there is an edge between nodes.

        Specifying `node` and `label` tests whether `node` has an out-edge with `label`.

        Three parameters tests for `target-target-label` edge membership.

        Specifying `edge_id` tests whether there is an edge with that id.

        Specifying `edge_id` with `node`, `target`, or `label` (or any combination)
        tests whether an edge with that id exists with signature `(node, target, label)`.
        """
        assert digraph.has('John')
        assert digraph.has('Rob')

        assert digraph.has('John', 'Mary', 'likes')
        assert digraph.has('Peter', 'Sarah', 'likes')

        assert digraph.has('John', label='likes')
        assert digraph.has('John', 'Mary')

        assert not digraph.has('Sarah', 'Peter', 'likes')
        assert not digraph.has('George')

        assert digraph.has(edge_id='jml')
        assert not digraph.has(edge_id='ood')

    def targets(digraph, source, label=None):
        """
        Get all of the _targets along out-edges of a given target.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.targets('Peter')) == {'John', 'Sarah'}

    def sources(digraph, target, label=None):
        """
        Get all of the sources along in-edges of a given target.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.sources('Mary')) == {'John'}

    def labels(digraph, source=None, target=None):
        """
        Get the edge labels associated with a (source, target) pair.
        """
        assert set(digraph.labels('John', 'Mary')) == {'likes'}

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
        oe = set(digraph.out_edges('Peter'))
        cmp = {('Peter', 'John', 'likes', 'pjl'), ('Peter', 'Sarah', 'likes', 'psl')}
        assert oe == cmp

    def in_edges(digraph, target, label=None):
        """
        Return an iterable over all in-edges of `target`.

        Providing a label filters the results based on edge label.
        """
        assert set(digraph.in_edges('Mary')) == {('John', 'Mary', 'likes', 'jml')}

    def source(digraph, edge_id):
        """
        Get the source of a specific edge by edge id.
        """
        assert digraph.source('jml') == 'John'

    def target(digraph, edge_id):
        """
        Get the target of a specific edge by edge id.
        """
        assert digraph.target('jml') == 'Mary'

    def label(digraph, edge_id):
        """
        Get the label of a specific edge by edge id.
        """
        assert digraph.label('jml') == 'likes'

    def signature(digraph, edge_id):
        """
        Get the source, target, and label of an edge as a tuple.
        """
        assert digraph.signature('jml') == ('John', 'Mary', 'likes')

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
                ('John', 'Mary', 'likes', 'jml'),
                ('Mary', 'Peter', 'likes', 'mpl'),
                ('Peter', 'John', 'likes', 'pjl'),
                ('Peter', 'Sarah', 'likes', 'psl')
        }

        assert set(digraph.edges('Mary')) == {
            ('John', 'Mary', 'likes', 'jml'),
            ('Mary', 'Peter', 'likes', 'mpl')
        }

        assert set(digraph.edges(label='likes')) == {
            ('John', 'Mary', 'likes', 'jml'),
            ('Mary', 'Peter', 'likes', 'mpl'),
            ('Peter', 'John', 'likes', 'pjl'),
            ('Peter', 'Sarah', 'likes', 'psl')
        }

    def add(digraph, node, target=None, label=None, edge_id=None):
        """
        Add a node or edge.

        One parameter adds a node.

        Four parameters adds an edge.

        Adding an edge without an id specified will automatically
        generate an id for that edge.
        """
        digraph.add('George')
        assert digraph.has('George')

        digraph.add('George', 'Rick', 'dislikes')
        assert digraph.has('George', 'Rick', 'dislikes')

        digraph.add('Mary', 'George', 'None', 'mgn')
        assert digraph.has('Mary', 'George', 'None')

        # More than one edge is allowed between two nodes
        digraph.add('John', 'Mary', 'dislikes', 'jmd')
        assert digraph.has('John', 'Mary', 'likes')
        assert digraph.has('John', 'Mary', 'dislikes')

        # More than one source,target,edge is allowed of the same signature
        digraph.add('John','store','go','jsg1')
        digraph.add('John', 'store', 'go', 'jsg2')
        assert digraph.has('John', 'store', 'go', 'jsg1')
        assert digraph.has('John', 'store', 'go', 'jsg2')

    def remove(digraph, node=None, target=None, label=None, edge_id=None):
        """
        Remove a node or edge.

        If only `node` is specified, removes that node and all connected edges.

        If `node` and `target` are specified, all out-edges from 'node' to 'target'.

        If `node`, `target`, and `label` are specified, removes all edges from `node`
        to `target` with `label`.

        If only `edge_id` is specified (or a `(s, t, l, id)` signature), removes a single edge.
        """
        digraph.remove('Rick')
        assert not digraph.has('Rick')
        assert not digraph.has('George', 'Rick', 'dislikes')
        assert digraph.has('George')

        digraph.remove(edge_id='mgn')
        assert not digraph.has('Mary', 'George', 'None')

        digraph.remove('John', 'Mary', 'likes')
        assert not digraph.has('John', 'Mary', 'likes')
        assert digraph.has('John', 'Mary', 'dislikes')

        digraph.remove('John', 'store')
        assert not digraph.has('John', 'store')

    def set(digraph, old, new):
        """
        Replaces a node.
        """
        digraph.set('Peter', 'Pete')
        assert not digraph.has('Peter')
        assert digraph.has('Pete')
        assert digraph.has('Pete', 'Sarah', 'likes')

    def set_label(digraph, label, edge_id=None):
        """
        Replaces the edge label of edge with id `edge_id` with `label`.
        """
        digraph.set_label('dislikes', 'psl')
        assert not digraph.has('Pete', 'Sarah', 'likes', 'psl')
        assert digraph.has('Pete', 'Sarah', 'dislikes', 'psl')

