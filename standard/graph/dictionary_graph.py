from standard.graph.graph import Graph

class DictionaryGraph(Graph):

    def __init__(self):
        self._nodes = {}

    def add_node(self, node):
        if node not in self._nodes:
            self._nodes[node] = {}