import standard.graph.core.tree as tree
from standard.graph.core.point_sequence import PointSequence

class Sequence(tree.Tree, PointSequence):
    """
    A linear, complete ordering of nodes, where ordering is represented by
    arc direction

    Constructor should expect an iterable as input where the first element
    yielded is the root of the Sequence and the last is the top

    Default members:

    `self._root`: the root (start) of the `Sequence`

    `self._top`: the top (end) of the `Sequence`
    """

    def __init__(self, iterable=None):
        PointSequence.__init__(self, iterable)

    def traverse(self, start=None):
        """
        Traverse the sequence in the forward direction, starting at node `start`
        """
        return PointSequence.traverse(self, start)

    def traverse_reverse(self, start=None):
        """
        Traverse the sequence in reverse, starting at node `start`
        """
        return PointSequence.traverse_reverse(self, start)

