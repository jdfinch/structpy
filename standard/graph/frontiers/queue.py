from standard.graph.sequence import Sequence
from standard.graph.frontiers.frontier_sequence import FrontierSequence
from standard.utilities.simple import rfind
from collections import deque

class Queue(FrontierSequence):
    """
    First-in-first-out sequence of nodes functioning as a .add/.pop collection

    Arcs in the Queue point from recently-inserted nodes to more historical
    nodes, with the next node in the queue being the `.top` of the Queue
    """

    def __init__(self, iterable):
        self._nodes = deque(iterable)

    def end(self):
        """
        Returns the next node in the Queue, or None if the Queue is empty
        """
        if self._nodes:
            return self._nodes[0]

    def pop(self):
        """
        Returns the latest-added node (on left)
        """
        return self._nodes.popleft()

    def add(self, node, epi=None, arc=None):
        """
        Adds node to the end of the queue, or adds epi if epi is specified
        and node is the last item in the current queue
        """
        if epi is None:
            self._nodes.append(node)
        elif node is self._nodes[-1]:
            self._nodes.append(epi)

    def add_node(self, node):
        """
        Adds a node, automatically the node will be placed at the end of the
        list and an arc will be added connecting it to the previous node
        """
        self._nodes.append(node)

    def add_arc(self, pro, epi, arc=True):
        """
        Adding an arc to the Queue may create a non-Sequence
        """
        raise NotImplementedError()

    def remove_node(self, node):
        """
        Uses list.remove to remove a node
        """
        self._nodes.remove(node)

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
        pro_index = rfind(self._nodes, pro)
        epi_index = rfind(self._nodes, epi)
        if epi_index != 1 + pro_index:
            return (pro, epi)
        return None

    def node_at(self, index):
        """
        Returns the node at a certain index, where the root is index 0
        """
        return self._nodes.__getitem__(index)

    def __iter__(self):
        return self._nodes.__iter__()

    def __next__(self):
        return self._nodes.__next__()

    def __getitem__(self, index):
        return self._nodes.__getitem__(index)

    def __str__(self):
        return 'Queue(' + ','.join([str(e) for e in self._nodes]) + ')'
