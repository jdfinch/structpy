
from structpy.graph.frontiers.frontier import Frontier
from structpy.graph.core.sequence import Sequence

class FrontierSequence(Sequence, Frontier):
    """
    Frontier for traversals
    """

    def complete(self):
        """
        Default implementation returning whether the Sequence is empty
        """
        return self.nodes_number() == 0

    def pop(self):
        """
        Default implementation to return the next node in the Frontier by
        removing and returning the `end` of the Sequence
        """
        node = self.top()
        self.remove_node(node)
        return node