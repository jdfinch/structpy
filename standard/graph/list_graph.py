from standard.graph.core.graph import Graph


class ListGraph(Graph):

    def __init__(self):
        self._nodes = {}
        self._reverse = {}

    def arcs(self):
        for node in self._nodes:
            node_neighbors = self._nodes[node]
            for other in node_neighbors:
                yield node_neighbors[other]

    def has_node(self, node):
        return node in self._nodes

    def has_arc(self, pro, epi):
        return pro in self._nodes and epi in [arc[0] for arc in self._nodes[pro]]

    def nodes_number(self):
        return len(self._nodes)

    def add_node(self, node):
        self._nodes[node] = []
        self._reverse[node] = set()

    def add_arc(self, pro, epi, arc=True):
        self._nodes[pro].append([epi,arc])
        self._reverse[epi].add(pro)

    def remove_node(self, node):
        del self._nodes[node]

        epis = self._nodes[node]
        for epi in epis:
            del self._reverse[epi][node]

        for other in self._nodes:
            idx = [arc[0] for arc in self._nodes[other]].index(node)
            if idx != -1:
                del self._nodes[other][idx]

    def remove_arc(self, pro, epi):
        del self._reverse[epi][pro]
        i = 0
        for arc in self._nodes[pro]:
            if arc[0] == epi:
                del self._nodes[pro][i]
                return

    def replace_node(self, old, new):
        self._nodes[new] = self._nodes[old]
        del self._nodes[old]

    def epis(self, node):
        for arc in self._nodes[node]:
            yield arc[0]

    def epis_number(self, node):
        return len(self._nodes[node])

    def arc(self, pro, epi):
        for arc in self._nodes[pro]:
            if arc[0] == epi:
                return arc[1]

    def arcs_out(self, pro):
        for arc in self._nodes[pro]:
            yield arc[1]

    def pros(self, node):
        for pro in self._reverse[node]:
            yield pro

    def pros_number(self, node):
        return len(self._reverse[node])

    def arcs_in(self, node):
        for arc in self._reverse[node].values():
            yield arc





