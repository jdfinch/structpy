
from structpy.graph.core.multi_graph import MultiGraph
from structpy.graph.flex.flex_graph import FlexGraph

class MultiFlexGraph(MultiGraph, FlexGraph):
    """
    `self._arcs dict<pro:dict<epi:set<arc>>>`
    `self._reverse: dict<epi:set<pro>>`
    `self._paths: dict<pro:dict<arc:set<epi>>>`
    `self._reverse_paths: dict<epi:dict<arc:set<pro>>>`
    """

    def __init__(self):
        FlexGraph.__init__(self)

    def arcs_between(self, pro, epi):
        return self._arcs[pro][epi]

    def num_arcs_between(self, pro, epi):
        return len(self._arcs[pro][epi])

    def nodes(self):
        return FlexGraph.nodes(self)

    def arcs(self):
        for pro, arc_epi in self._arcs.items():
            for epi, arcs in arc_epi.items():
                for arc in arcs:
                    yield (pro, epi, arc)

    def has_node(self, node):
        return FlexGraph.has_node(self, node)

    def has_arc(self, pro, epi):
        return FlexGraph.has_arc(self, pro, epi)

    def nodes_number(self):
        return FlexGraph.nodes_number(self)

    def arcs_number(self):
        return FlexGraph.arcs_number(self)

    def add_node(self, node):
        return FlexGraph.add_node(self, node)

    def add_arc(self, pro, epi, arc=True):
        if epi in self._arcs[pro]:
            self._arcs[pro][epi].add(arc)
        else:
            self._arcs[pro][epi] = {arc}
            self._reverse[epi].add(pro)
        if arc not in self._paths[pro]:
            self._paths[pro][arc] = {epi}
        else:
            self._paths[pro][arc].add(epi)
        if arc not in self._reverse_paths[epi]:
            self._reverse_paths[epi][arc] = {pro}
        else:
            self._reverse_paths[epi][arc].add(pro)
        self._arcs_number += 1

    def remove(self, node, epi=None, arc_value=None):
        if epi is None:
            self.remove_node(node)
        else:
            self.remove_arc(node, epi, arc_value)

    def remove_node(self, node):
        for pro in self._reverse[node]:
            arcs = self._arcs[pro][node]
            del self._arcs[pro][node]
            for arc in arcs:
                self._paths[pro][arc].remove(node)
            self._arcs_number -= len(arcs)
        for epi, arcs in self._arcs[node].items():
            self._reverse[epi].remove(node)
            for arc in arcs:
                self._reverse_paths[epi][arc].remove(node)
            self._arcs_number -= len(arcs)
        del self._reverse[node]
        del self._arcs[node]

    def remove_all_arcs(self, pro, epi):
        arcs = self._arcs[pro][epi]
        del self._arcs[pro][epi]
        self._reverse[epi].remove(pro)
        for arc in arcs:
            self._paths[pro][arc].remove(epi)
            self._reverse_paths[epi][arc].remove(pro)
        self._arcs_number -= len(arcs)

    def remove_arc(self, pro, epi, arc_value=None):
        arcs = self._arcs[pro][epi]
        if arcs == {arc_value} or arc_value is None:
            self.remove_all_arcs(pro, epi)
        else:
            arcs.remove(arc_value)
            self._paths[pro][arc_value].remove(epi)
            self._reverse_paths[epi][arc_value].remove(pro)
            self._arcs_number -= 1

    def epis(self, node, arc_value=None):
        return FlexGraph.epis(self, node, arc_value)

    def pros(self, node, arc_value=None):
        return FlexGraph.pros(self, node, arc_value)

    def epis_number(self, node):
        return FlexGraph.epis_number(self, node)

    def pros_number(self, node):
        return FlexGraph.pros_number(self, node)




























