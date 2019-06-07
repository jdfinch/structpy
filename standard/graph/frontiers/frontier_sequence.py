
from standard.graph.frontiers.frontier import Frontier
from standard.graph.sequence import Sequence

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
        node = self.end()
        self.remove_node(node)
        return node