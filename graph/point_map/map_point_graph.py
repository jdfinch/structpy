
from structpy.graph.core.point_graph import PointGraph

class MapPointGraph(PointGraph):
    """
    `self._nodes`: dict<pro:set<epi>>
    `:self._reverse`:dict<epi:set<pro>>
    """

    def __init__(self):
        self._nodes = {}
        self._reverse = {}

    def arcs(self):
        for node in self._nodes:
            for epi in self._nodes[node]:
                yield (node, epi)

    def has_arc(self, pro, epi):
        return epi in self._nodes[pro]

    def nodes_number(self):
        return len(self._nodes)

    def arcs_number(self):
        i = 0
        for _, epis in self._nodes.items():
            i += len(epis)
        return i

    def add_node(self, node):
        self._nodes[node] = set()
        self._reverse[node] = set()

    def add_arc(self, pro, epi, arc=None):
        self._nodes[pro].add(epi)
        self._reverse[epi].add(pro)

    def remove_node(self, node):
        for epi in self._nodes[node]:
            self._reverse[epi].remove(node)
        del self._nodes[node]
        for pro in self._reverse[node]:
            self._nodes[pro].remove(node)
        del self._nodes[node]

    def remove_arc(self, pro, epi):
        self._nodes[pro].remove(epi)
        self._reverse[epi].remove(pro)

    def epis(self, node):
        if node in self._nodes:
            for epi in self._nodes[node]:
                yield epi

    def epis_number(self, node):
        if node in self._nodes:
            return len(self._nodes[node])
        else:
            return 0

    def pros(self, node):
        if node in self._reverse:
            for pro in self._reverse[node]:
                yield pro

    def pros_number(self, node):
        if node in self._reverse:
            return len(self._reverse[node])
        else:
            return 0