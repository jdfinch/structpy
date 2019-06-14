from standard.graph.graph import Graph

class DictionaryGraph(Graph):

    def __init__(self):
        self._nodes = {}

    def arcs(self):
        for node in self._nodes:
            node_neighbors = self._nodes[node]
            for other in node_neighbors:
                yield node_neighbors[other]
    
    def has_node(self, node):
        return node in self._nodes

    def has_arc(self, pro, epi):
        return pro in self._nodes and epi in self._nodes[pro]

    def nodes_number(self):
        return len(self._nodes)

    def add_node(self, node):
        self._nodes[node] = {}

    def add_arc(self, pro, epi, arc=True):
        self._nodes[pro][epi] = arc

    def remove_node(self, node):
        del self._nodes[node]
        for other in self._nodes:
            if node in self._nodes[other]:
                del self._nodes[other][node]
        
    def remove_arc(self, pro, epi):
        del self._nodes[pro][epi]

    def replace_node(self, old, new):
        self._nodes[new] = self._nodes[old]
        del self._nodes[old]

    '''
    Re-introduce later for efficiency
    
    def replace_arc(self, pro, epi, new):
        self._nodes[pro][epi] = new
    
    def replace_arc_epi(self, pro, epi, new_epi):
        self._nodes[pro][new_epi] = self._nodes[pro][epi]
        del self._nodes[pro][epi]

    def replace_arc_pro(self, pro, epi, new_pro):
        self._nodes[new_pro][epi] = self._nodes[pro][epi]
        del self._nodes[pro][epi]
    '''

    def epis(self, node):
        for epi in self._nodes[node]:
            yield epi
    
    def epis_number(self, node):
        return len(self._nodes[node])

    def arc(self, pro, epi):
        try:
            return self._nodes[pro][epi]
        except KeyError:
            return None

    def arcs_out(self, pro):
        for arc in self._nodes[pro].values():
            yield arc



    
    
