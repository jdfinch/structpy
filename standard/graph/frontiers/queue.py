from standard.graph.sequence import Sequence
from standard.graph.frontiers.frontier_sequence import FrontierSequence
from standard.utilities.simple import rfind
import standard.collections as stdcol

class Queue(FrontierSequence, stdcol.Queue):
    """
    First-in-first-out sequence of nodes functioning as a .add/.pop collection

    Arcs in the Queue point from recently-inserted nodes to more historical
    nodes, with the next node in the queue being the `.top` of the Queue
    """

    def __init__(self, iterable=None):
        stdcol.Queue.__init__(self)
        if iterable is not None:
            for e in iterable:
                self.add(e)

    top = stdcol.Queue.top

    pop = stdcol.Queue.pop

    def nodes(self):
        for node in self:
            yield node

    def add(self, node, epi=None, arc=None):
        """
        Adds node to the end of the queue, or adds epi if epi is specified
        and node is the last item in the current queue
        """
        if epi is None:
            stdcol.Queue.add(self, node)
        elif node is self[-1]:
            stdcol.Queue.add(self, epi)

    def add_node(self, node):
        """
        Adds a node, automatically the node will be placed at the end of the
        list and an arc will be added connecting it to the previous node
        """
        stdcol.Queue.add(self, node)

    def add_arc(self, pro, epi, arc=True):
        """
        Adding an arc to the Queue may create a non-Sequence
        """
        raise NotImplementedError()

    def remove_node(self, node):
        """
        Uses list.remove to remove a node
        """
        stdcol.Queue.remove(self, node)

    def remove_arc(self, pro, epi):
        """
        Removing an arc from the Queue may create a non-Sequence
        """
        raise NotImplementedError()

    def arc(self, pro, epi):
        """
        Returns a tuple (pro, epi) if epi follows pro in the list,
        otherwise None
        """
        pro_index = rfind(self, pro)
        epi_index = rfind(self, epi)
        if epi_index != 1 + pro_index:
            return (pro, epi)
        return None

    def node_at(self, index):
        """
        Returns the node at a certain index, where the root is index 0
        """
        return stdcol.Queue.__getitem__(self, index)

    def __str__(self):
        return 'Queue(' + ','.join([str(e) for e in self._nodes]) + ')'
