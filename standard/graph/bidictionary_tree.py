from standard.graph.bidictionary_graph import BidictionaryGraph
from standard.graph.tree import Tree

class BidictionaryTree(BidictionaryGraph, Tree):

    def __init__(self, root):
        BidictionaryGraph.__init__(self)
        Tree.__init__(self, root)
