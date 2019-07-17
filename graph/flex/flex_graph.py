
from structpy.graph.core.graph import Graph

class FlexGraph(Graph):
    """
    `self._arcs dict<pro:dict<epi:arc>>`
    `self._reverse: dict<epi:set<pro>>`
    `self._paths: dict<pro:dict<arc:set<epi>>>`
    """

    def __init__(self):
        self._arcs = {}
        self._reverse = {}
        self._paths = {}
        self._reverse_paths = {}
        self._arcs_number = 0

    def nodes(self):
        return iter(self._arcs.keys())

    def arcs(self):
        for pro, arc_epi in self._arcs.items():
            for epi, arc in arc_epi.items():
                yield (pro, epi, arc)

    def has_node(self, node):
        return node in self._arcs

    def has_arc(self, pro, epi):
        return pro in self._arcs and epi in self._arcs[pro]

    def nodes_number(self):
        return len(self._arcs)

    def arcs_number(self):
        return self._arcs_number

    def add_node(self, node):
        self._arcs[node] = {}
        self._reverse[node] = set()
        self._paths[node] = {}
        self._reverse_paths[node] = {}

    def add_arc(self, pro, epi, arc=True):
        self._arcs[pro][epi] = arc
        self._reverse[epi].add(pro)
        if arc not in self._paths[pro]:
            self._paths[pro][arc] = set()
        self._paths[pro][arc].add(epi)
        if arc not in self._reverse_paths[epi]:
            self._reverse_paths[epi][arc] = set()
        self._reverse_paths[epi][arc].add(pro)
        self._arcs_number += 1

    def remove_node(self, node):
        for pro in self._reverse[node]:
            arc = self._arcs[pro][node]
            del self._arcs[pro][node]
            self._paths[pro][arc].remove(node)
        for epi, arc in self._arcs[node].items():
            self._reverse[epi].remove(node)
            self._reverse_paths[epi][arc].remove(node)
        self._arcs_number -= len(self._reverse[node])
        del self._reverse[node]
        self._arcs_number -= len(self._arcs[node])
        del self._arcs[node]

    def remove_arc(self, pro, epi):
        arc = self._arcs[pro][epi]
        del self._arcs[pro][epi]
        self._reverse[epi].remove(pro)
        self._paths[pro][arc].remove(epi)
        self._reverse_paths[epi][arc].remove(pro)
        self._arcs_number -= 1

    def epis(self, node, arc_value=None):
        if arc_value is None:
            yield from self._arcs[node]
        path = self._paths[node]
        if arc_value not in path:
            return
        yield from path[arc_value]

    def pros(self, node, arc_value=None):
        if arc_value is None:
            yield from self._reverse[node]
        path = self._reverse_paths[node]
        if arc_value not in path:
            return
        yield from path[arc_value]

    def epis_number(self, node):
        return len(self._arcs[node])

    def pros_number(self, node):
        return len(self._reverse[node])

    def arc(self, pro, epi):
        if epi in self._arcs[pro]:
            return self._arcs[pro][epi]