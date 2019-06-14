from standard.graph.list_graph import ListGraph
from standard.graph.tree import Tree

class ListTree(ListGraph, Tree):

    def __init__(self, root):
        ListGraph.__init__(self)
        Tree.__init__(self, root)