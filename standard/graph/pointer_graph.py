from standard.graph.core.graph import Graph

class PointerGraph(Graph):

    def __init__(self):
        self._nodes = {}

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
        for arc in self.arcs():
            i += 1
        return i

    def add_node(self, node):
        self._nodes[node] = set()

    def add_arc(self, pro, epi, arc=None):
        self._nodes[pro].add(epi)

    def remove_node(self, node):
        del self._nodes[node]
        for other in self._nodes:
            if node in self._nodes[other]:
                self._nodes[other].remove(node)
    
    def remove_arc(self, pro, epi):
        self._nodes[pro].remove(epi)

    def epis(self, node):
        if node in self._nodes:
            for node in self._nodes[node]:
                yield node
    
    def epis_number(self, node):
        if node in self._nodes:
            return len(self._nodes[node])
        else:
            return 0

    def arc(self, pro, epi):
        if pro in self._nodes and epi in self._nodes[pro]:
            return (pro, epi)
        else:
            return None

    def pro(self, arc):
        return arc[0]
    
    def epi(self, arc):
        return arc[1]
