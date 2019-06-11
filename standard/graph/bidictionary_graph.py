from standard.graph.dictionary_graph import DictionaryGraph

class BidictionaryGraph(DictionaryGraph):
    """
    Dictionary graph with backpointers for efficient reverse traversal

    Backpointers are implemented as elements in a `set`
    """

    def __init__(self):
        DictionaryGraph.__init__(self)
        self._reverse = {}

    def add_node(self, node):
        DictionaryGraph.add_node(self, node)
        self._reverse[node] = set()

    def add_arc(self, pro, epi, arc=True):
        DictionaryGraph.add_arc(self, pro, epi, arc)
        self._reverse[epi].add(pro)

    def remove_node(self, node):
        epis = self._nodes[node]
        pros = self._reverse[node]
        del self._nodes[node]
        for epi in epis:
            del self._reverse[epi][node]
        for pro in pros:
            del self._nodes[pro][node]

    def remove_arc(self, pro, epi):
        del self._nodes[pro][epi]
        del self._reverse[epi][pro]

    def pros(self, node):
        for pro in self._reverse[node]:
            yield pro

    def pros_number(self, node):
        return len(self._reverse[node])

    def arcs_in(self, node):
        for arc in self._reverse[node].values():
            yield arc

