
from structpy.graph.core.graph import Graph

class CompoundGraph(Graph):

    def __init__(self, A, B):
        """

        :param A: first graph object
        :param B: second graph object
        """
        self._A = A
        self._B = B

    def first_graph(self):
        return self._A

    def second_graph(self):
        return self._B

    def nodes(self):
        return set(self.first_graph().nodes()) \
               | set(self.second_graph().nodes())
    
    def arcs(self):
        return set(self.first_graph().arcs()) \
               | set(self.second_graph().arcs())

    def nodes_number(self):
        return len(self.nodes())

    def arcs_number(self):
        return len(self.arcs())
    
    def has_node(self, node):
        return self.first_graph().has_node(node) \
               or self.second_graph().has_node(node)
    
    def has_arc(self, pro, epi):
        return self.first_graph().has_arc(pro, epi) \
               or self.second_graph().has_arc(pro, epi)
    
    def arc(self, pro, epi):
        if self.first_graph().has_arc(pro, epi):
            return self.first_graph().arc(pro, epi)
        if self.second_graph().has_arc(pro, epi):
            return self.second_graph().arc(pro, epi)
        
    def has_arc_value(self, arc):
        return self.first_graph().has_arc_value(arc) \
               or self.second_graph().has_arc_value(arc)
    
    def add_node(self, node):
        self.first_graph().add_node(node)
        self.second_graph().add_node(node)
        
    def add_arc(self, pro, epi, arc=True):
        self.first_graph().add_arc(pro, epi, arc)
        self.second_graph().add_arc(pro, epi, arc)
        
    def epis(self, node, arc_value=None):
        return set(self.first_graph().epis(node, arc_value)) \
               | set(self.second_graph().epis(node, arc_value))
        
    def pros(self, node, arc_value=None):
        return set(self.first_graph().pros(node, arc_value)) \
               | set(self.second_graph().pros(node, arc_value))

    def epis_number(self, node, arc_value=None):
        return len(self.epis(node, arc_value))

    def pros_number(self, node, arc_value=None):
        return len(self.pros(node, arc_value))

