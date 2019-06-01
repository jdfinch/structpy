
graph_full_template = \
'''
from standard.graph import Graph

class MyGraph(Graph):
    
    def __init__(self):
        self._nodes = 
        self._arcs = 

    def nodes(self):
        """Iterates over all nodes in the graph"""
        return Graph.nodes(self)

    def arcs(self):
        """Iterates over all arcs in the graph."""
        return Graph.arcs(self)

    def arcs_out(self, node):
        """Iterates over the arcs that the node is a pro of"""
        return Graph.arcs_out(self, node)

    def arcs_in(self, node):
        """Iterates over the arcs that the node is an epi of"""
        return Graph.arcs_in(self, node)

    def arc(self, pro, epi):
        """Returns the arc from pro to epi, or None if none exists"""
        return Graph.arc(self, pro, epi)

    def has_node(self, node):
        """Returns boolean indicating whether the graph contains node"""
        return Graph.has_node(self, node)

    def has_arc(self, arc):
        """Returns boolean indicating whether the graph contains arc"""
        return Graph.has_arc(self, arc)

    def pro(self, arc):
        """Returns the pro of arc"""
        return Graph.pro(self, arc)

    def epi(self, arc):
        """Returns the epi of arc"""
        return Graph.epi(self, arc)

    def add_node(self, node):
        """Add a node to the graph, initialized without any arcs"""
        return Graph.add_node(self, node)

    def add_arc(self, pro, epi, arc=True):
        """Add an arc from pro to epi to the graph. By default, unlabeled arcs are
        valued True. Does not add pro or epi to the graph explicitly"""
        return Graph.add_arc(self, pro, epi, arc)

    def epis(self, node):
        """Return the epis that node has arcs to"""
        return Graph.epis(self, node)

    def pros(self, node):
        """Return the pros that have arcs where node is the epi"""
        return Graph.pros(self, node)

    def remove_node(self, node):
        """Remove node from the graph"""
        raise NotImplementedError('Implement remove_node to enable removal')

    def remove_arc(self, pro, epi):
        """Remove an arc from the graph by specifying its pro and epi"""
        raise NotImplementedError('Implement remove_arc to enable removal')
'''