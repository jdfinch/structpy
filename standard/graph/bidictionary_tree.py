from standard.graph.bidictionary_graph import BidictionaryGraph
from standard.graph.core.tree import Tree

class BidictionaryTree(BidictionaryGraph, Tree):

    def __init__(self, root=None):
        BidictionaryGraph.__init__(self)
        Tree.__init__(self, root)
