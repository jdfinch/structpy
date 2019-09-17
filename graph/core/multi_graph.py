
from structpy.graph.core.graph import Graph
from structpy.graph.core.point_graph import PointGraph

class MultiGraph(Graph):

    def arc(self, pro, epi):
        """
        Returns the arc from pro to epi, or None if none exists

        Guideline implementation: return a tuple `(pro, epi, arc_value)`, or
        `(pro, epi)` if the arc is valueless

        Default implementation: iterates over `self.arcs()` and returns an arc
        where `self.pro(arc)` and `self.epi(arc)` match pro and epi
        respectively. O(T(`self.pro`) * T(`self.epi`) * T(`self.arc`))
        """
        return {arc for arc in self.arcs_between(pro, epi)}

    def has_arc(self, pro, epi):
        """
        Returns boolean indicating whether the graph contains arc

        Default implementation: routes to `self.arc`
        O(T(`self.arc`))
        """
        if self.arc(pro, epi):
            return True
        return False

    def arcs_between(self, pro, epi, arc_value=None):
        if arc_value is None:
            for p, e, a in self.arcs():
                if p is pro and e is epi:
                    yield a
        else:
            for p, e, a in self.arcs():
                if p is pro and e is epi and a is arc_value:
                    yield a

    def num_arcs_between(self, pro, epi, arc_value=None):
        i = 0
        for _ in self.arcs_between(pro, epi, arc_value):
            i += 1
        return i

    def pros(self, node, arc_value=None):
        """
        Get the pros of the node, optionally filtering by an arc value
        :param node: node in the graph
        :param arc_value: value that arcs have to be equal to between this
                          node and the pro for the pro to be yielded
        :return: generator over pros
        """
        if arc_value is None:
            yield from PointGraph.pros(self, node)
        for pro in PointGraph.pros(self, node):
            if arc_value in self.arc(pro, node):
                yield pro

    def epis(self, node, arc_value=None):
        """
        Get the epis of the node, optionally filtering by an arc value
        :param node: node in the graph
        :param arc_value: value that arcs have to be equal to between this
                          node and the epi for the epi to be yielded
        :return: generator over epis
        """
        if arc_value is None:
            yield from PointGraph.epis(self, node)
        for epi in PointGraph.epis(self, node):
            if arc_value in self.arc(node, epi):
                yield epi

    def replace_pro(self, pro, epi, new_pro):
        for arc in self.arcs_between(pro, epi):
            self.remove_arc(pro, epi)
            self.add_arc(new_pro, epi, arc)

    def replace_epi(self, pro, epi, new_epi):
        for arc in self.arcs_between(pro, epi):
            self.remove_arc(pro, epi)
            self.add_arc(pro, new_epi, arc)

    def replace_node(self, old, new):
        """
        replace old node with new while preserving arcs and their types
        :param new:
        :param old:
        :return:
        """
        if not self.has_node(new):
            self.add_node(new)
        for pro in self.pros(old):
            for arc in self.arcs_between(pro, old):
                self.add_arc(pro, new, arc)
        for epi in self.epis(old):
            for arc in self.arcs_between(old, epi):
                self.add_arc(new, epi, arc)
        self.remove_node(old)















