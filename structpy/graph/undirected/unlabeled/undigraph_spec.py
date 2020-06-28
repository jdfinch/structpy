
from structpy import specification


@specification
class UndigraphSpec:
    """
    Undirected, unlabeled undigraph.

    Each node must be a unique hashable object.

    Arcs are identified by node pairs, which are unordered.
    Therefore, arc `A-B` is the same as arc `B-A`.
    """

    @specification.init
    def UNDIGRAPH(Undigraph):
        """
        Creates an empty Undigraph.

        Nodes and arcs are added using the `add` method.
        """
        undigraph = Undigraph(arcs=[
            ('a', 'b'),
            ('b', 'c'),
            ('c', 'd')
        ])
        return undigraph

    def add_node(undigraph, node):
        """
        Add a node to the undigraph.
        """
        undigraph.add_node('e')

    def add_arc(undigraph, node, neighbor):
        """
        Add an arc between existing nodes in the undigraph.
        Has no effect if the arc already exists.
        """
        undigraph.add_arc('d', 'e')


    def add(undigraph, node, neighbor=None):
        """
        Add a node, or an arc to the undigraph.
        If an arc is added between two nodes that do not
        already exist, they are added automatically.
        """
        undigraph.add('c', 'f')


    def remove_node(undigraph, node):
        """
        Remove a node from the undigraph, if it exists.
        This will remove all arcs that contain the removed node.
        """
        undigraph.remove_node('a')


    def remove_arc(undigraph, node, neighbor):
        """
        Remove an arc from the undigraph, if it exists.
        """
        undigraph.remove_arc('b', 'c')


    def remove(undigraph, node, neighbor=None):
        """
        Remove either a node or an arc from the undigraph.

        If adjecent node is not specified, a node will be
        removed along with all of its arcs.
        """
        undigraph.remove('c', 'd')


    def has_node(undigraph, node):
        """
        Whether a node is in the undigraph.
        """
        assert undigraph.has_node('b')
        assert undigraph.has_node('e')
        assert undigraph.has_node('f')
        assert not undigraph.has_node('a')


    def has_arc(undigraph, node, neighbor):
        """
        Whether an arc is in the undigraph.
        """
        assert not undigraph.has_arc('b', 'c')
        assert undigraph.has_arc('d', 'e')
        assert undigraph.has_arc('c', 'f')
        assert not undigraph.has_arc('a', 'f')


    def has(undigraph, node, neighbor=None):
        """
        Whether a node is in the undigraph or, if neighbor is specified,
        whether the arc between node and neighbor is in the undigraph.
        """
        assert not undigraph.has('b', 'c')
        assert undigraph.has('d', 'e')
        assert not undigraph.has('a')
        assert undigraph.has('b')


    def nodes(undigraph):
        """
        A generator over the nodes in the undigraph, unordered.
        """
        assert set(undigraph.nodes()) == {'b', 'c', 'd', 'e', 'f'}


    def arcs(undigraph):
        """
        A generator over the arcs in the undigraph, unordered.
        """
        assert False


    def len_nodes(undigraph):
        """
        Returns the number of nodes in the undigraph.
        """
        assert undigraph.len_nodes() == 5


    def len_arcs(undigraph):
        """
        Returns the number of arcs in the undigraph.
        """
        assert undigraph.len_arcs() == 2


if __name__ == '__main__':
    print(UndigraphSpec.__verify__())

