
from structpy.language import spec, Implementation


@spec
class Undigraph:
    """
    Undirected, unlabeled graph.

    Each node must be a unique hashable object.

    Arcs are identified by node pairs, which are unordered.
    Therefore, arc `A-B` is the same as arc `B-A`.
    """

    __kwargs__ = {

    }

    @spec.init
    def INIT____Unidigraph(Graph):
        """
        Creates an empty Unidigraph.

        Nodes and arcs are added using the `add` method.
        """
        graph = Graph(arcs=[
            ('a', 'b'),
            ('b', 'c'),
            ('c', 'd')
        ])
        return graph

    @spec.prop
    def add_node(graph, node):
        """
        Add a node to the graph.
        """
        graph.add_node('e')

    @spec.prop
    def add_arc(graph, node, neighbor):
        """
        Add an arc between existing nodes in the graph.
        Has no effect if the arc already exists.
        """
        graph.add_arc('d', 'e')

    @spec.prop
    def add(graph, node, neighbor=None):
        """
        Add a node, or an arc to the graph.
        If an arc is added between two nodes that do not
        already exist, they are added automatically.
        """
        graph.add('c', 'f')

    @spec.prop
    def remove_node(graph, node):
        """
        Remove a node from the graph, if it exists.
        This will remove all arcs that contain the removed node.
        """
        graph.remove_node('a')

    @spec.prop
    def remove_arc(graph, node, neighbor):
        """
        Remove an arc from the graph, if it exists.
        """
        graph.remove_arc('b', 'c')

    @spec.prop
    def remove(graph, node, neighbor=None):
        """
        Remove either a node or an arc from the graph.

        If adjecent node is not specified, a node will be
        removed along with all of its arcs.
        """
        graph.remove('c', 'd')

    @spec.prop
    def has_node(graph, node):
        """
        Whether a node is in the graph.
        """
        assert graph.has_node('b')
        assert graph.has_node('e')
        assert graph.has_node('f')
        assert not graph.has_node('a')

    @spec.prop
    def has_arc(graph, node, neighbor):
        """
        Whether an arc is in the graph.
        """
        assert not graph.has_arc('b', 'c')
        assert graph.has_arc('d', 'e')
        assert graph.has_arc('c', 'f')
        assert not graph.has_arc('a', 'f')

    @spec.prop
    def has(graph, node, neighbor=None):
        """
        Whether a node is in the graph or, if neighbor is specified,
        whether the arc between node and neighbor is in the graph.
        """
        assert not graph.has('b', 'c')
        assert graph.has('d', 'e')
        assert not graph.has('a')
        assert graph.has('b')

    @spec.prop
    def nodes(graph):
        """
        A generator over the nodes in the graph, unordered.
        """
        assert set(graph.nodes()) == {'b', 'c', 'd', 'e', 'f'}

    @spec.prop
    def arcs(graph):
        """
        A generator over the arcs in the graph, unordered.
        """
        assert False

    @spec.prop
    def len_nodes(graph):
        """
        Returns the number of nodes in the graph.
        """
        assert graph.len_nodes() == 5

    @spec.prop
    def len_arcs(graph):
        """
        Returns the number of arcs in the graph.
        """
        assert graph.len_arcs() == 2


if __name__ == '__main__':
    Undigraph.__verify__()

